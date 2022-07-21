import logging
import os
import os.path
import sys
from base64 import b64encode
from gzip import compress
import json
from typing import Any, Dict, List, Text, Optional

# pip install --target ./site-packages -r requirements.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'site-packages'))

from .sentry_driver import process_row
from .utils import create_response, setup_sentry, format_row_dict

BATCH_ID_HEADER = 'sf-external-function-query-batch-id'
DESTINATION_URI_HEADER = 'sf-custom-destination-uri'

CONSOLE_LOGGER = logging.getLogger('console')
SENTRY_DRIVER_LOGGER = logging.getLogger('sentry_driver')


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
    response_data = []

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

    result_data_json = json.dumps({'data': result}, default=str)
    response = {
        'statusCode': 200,
        'body': b64encode(compress(result_data_json.encode())).decode(),
        'isBase64Encoded': True,
        'headers': {'Content-Encoding': 'gzip'}
    }
    print(response)
    return response


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
