import json
import logging
import os
import os.path
import sys
from base64 import b64encode
from gzip import compress
from typing import Any, Dict, List, Text

# pip install --target ./site-packages -r requirements.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'site-packages'))

from .sentry_driver import process_message, process_row
from .utils import create_response, format_row_dict, setup_dsn, setup_sentry

BATCH_ID_HEADER = 'sf-external-function-query-batch-id'
DESTINATION_URI_HEADER = 'sf-custom-destination-uri'

CONSOLE_LOGGER = logging.getLogger('console')
SENTRY_DRIVER_LOGGER = logging.getLogger('sentry_driver')


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
    CONSOLE_LOGGER.debug('lambda_handler() called.')
    dsn = setup_dsn(event)

    CONSOLE_LOGGER.debug(f'Setting up Sentry SDK for dsn: {dsn}.')
    setup_sentry(dsn)

    if 'Records' in event and len(event['Records']) > 0:
        return process_message(json.loads(event['Records'][0]['Sns']['Message']))
    return sync_flow(event, context)
