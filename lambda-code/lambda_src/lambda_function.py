import logging
import os
import os.path
import sys
from base64 import b64encode
from gzip import compress
import json
from typing import Any, Dict, List, Text, Optional
from datetime import date, timedelta
    
# pip install --target ./site-packages -r requirements.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'site-packages'))

from .sentry_driver import process_row
from .utils import create_response, setup_sentry, format_row_dict

BATCH_ID_HEADER = 'sf-external-function-query-batch-id'
DESTINATION_URI_HEADER = 'sf-custom-destination-uri'

CONSOLE_LOGGER = logging.getLogger('console')
SENTRY_DRIVER_LOGGER = logging.getLogger('sentry_driver')
AWS_REGION = os.environ.get('AWS_REGION')


def get_dsn(headers: Any, data: List[Any]) -> Optional[str]:
    """Return the first dsn

    Args:
        headers (Any): _description_
        data (List[Any]): _description_

    Returns:
        Optional[str]: _description_
    """
    dsn = None
    for row_number, *args in data:
        CONSOLE_LOGGER.debug(f'Processing row: {row_number}.')

        process_row_params = {
            k.replace('sf-custom-', '').replace('-', '_'): format_row_dict(v, args)
            for k, v in headers.items()
            if k.startswith('sf-custom-')
        }

        dsn = process_row_params.get('dsn')
        break
    return dsn


def sync_flow(event: Any, context: Any = None) -> Dict[Text, Any]:
    """
    Handles the synchronous part of the generic lambda flows.

    Args:
        event (Any): This the event object as received by the lambda_handler()
        context (Any): Has the function context. Defaults to None.

    Returns:
        Dict[Text, Any]: Represents the response status and data.
    """
    CONSOLE_LOGGER.debug('Using sync_flow().')

    headers = event['headers']
    request_body = json.loads(event['body'])
    response_data: List[Any] = []

    # Convert sf-custom- prefixed keys to regular keys without that prefix
    for row_number, *args in request_body['data']:
        CONSOLE_LOGGER.debug(f'Processing row: {row_number}.')

        process_row_params = {
            k.replace('sf-custom-', '').replace('-', '_'): format_row_dict(v, args)
            for k, v in headers.items()
            if k.startswith('sf-custom-')
        }
        process_row_params.pop('dsn')
        result = process_row(**process_row_params)
        response_data.append([row_number, result])

    result_data_json = json.dumps({'data': response_data}, default=str)
    response = {
        'statusCode': 200,
        'body': b64encode(compress(result_data_json.encode())).decode(),
        'isBase64Encoded': True,
        'headers': {'Content-Encoding': 'gzip'}
    }
    return response


def process_message(message: Any) -> Any:
    CONSOLE_LOGGER.debug(f"From SNS: {message}")

    pipe_full_name = message['pipeName']
    database, schema_and_pipe = pipe_full_name.split(".", 1)
    schema, pipe_name = schema_and_pipe.split(".", 1)

    history_type = 'COPY'
    error_msg = message['messages']['firstError']
    timestamp = message['timestamp']
    account_name = message['accountName']
    date_today = str(date.today())
    date_1_week_back = str(date.today() - timedelta(days=7))

    pipe_error_history_url: str = (
        f'https://app.snowflake.com/{AWS_REGION}/{account_name}/compute/history/copies?'
        + 'type=relative&relative={"tense":"past","value":7,"unit":"day","excludePartial":false,"exclusionSize":"day","exclusionSizeParam":""}' + f'&startDate={date_today}&endDate={date_1_week_back}'
        + '&status=LOAD_FAILED'
        + f'&database={database}'
        + f'&schema={schema}'
        + f'&pipe={pipe_name}&preset=PRESET_LAST_7_DAYS'
    )
    return process_row(
        pipe_name,
        history_type,
        error_msg,
        timestamp,
        pipe_error_history_url,
    )


def lambda_handler(event: Any, context: Any) -> Dict[Text, Any]:
    """
    Implements the asynchronous function on AWS as described in the Snowflake docs here:
    https://docs.snowflake.com/en/sql-reference/external-functions-creating-aws.html

    Args:
        event (Any): Event received from AWS
        context (Any): Function context received from AWS

    Returns:
        Dict[Text, Any]: Returns the response body.
    """
    method = event.get('httpMethod')

    if 'Records' in event and len(event['Records']) > 0:
        return process_message(json.loads(event['Records'][0]['Sns']['Message']))

    headers = event['headers']
    request_body = json.loads(event['body'])
    CONSOLE_LOGGER.debug(f'lambda_handler() called.')
    destination = headers.get(DESTINATION_URI_HEADER)
    dsn = get_dsn(headers, request_body['data'])
    CONSOLE_LOGGER.debug(f'Sentry DSN: {dsn}')

    if not dsn:
        return create_response(400, 'Sentry DSN is not set and is required to log errors to Sentry.')

    CONSOLE_LOGGER.debug(f'Setting up Sentry SDK for dsn: {dsn}.')
    setup_sentry(dsn)

    # httpMethod exists implies caller is API Gateway
    if method == 'POST' and destination:
        CONSOLE_LOGGER.warning('Async flow is not supported.')
    elif method == 'POST':
        return sync_flow(event, context)
    elif method == 'GET':
        CONSOLE_LOGGER.warning('Async flow is not supported.')

    return create_response(400, 'Unexpected Request.')
