import json
import logging
import os
import re
from typing import Any, Dict, Text

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from .log import setup_logger

ULILS_LOGGER = setup_logger('utils', logging.DEBUG)
DEFAULT_SNOWFLAKE_ERROR_DSN = os.environ['DEFAULT_SNOWFLAKE_ERROR_DSN']


def format_row_dict(s, ps):
    """format string s with params ps, preserving type of singular references

    >>> format_row_dict('{0}', [{'a': 'b'}])
    {'a': 'b'}

    >>> format_row_dict('{"z": [{0}]}', [{'a': 'b'}])
    """

    def replace_refs(s, ps):
        for i, p in enumerate(ps):
            old = '{' + str(i) + '}'
            new = json.dumps(p) if isinstance(p, (list, dict)) else str(p)
            s = s.replace(old, new)
        return s

    m = re.match(r'{(\d+)}', s)
    return ps[int(m.group(1))] if m else replace_refs(s, ps)


def error_response(code: int) -> Dict[str, object]:
    response = {}
    if code == 403:
        response = {
            'statusCode': 403,
            'body': json.dumps({'error': 'Unauthorized Request.'}),
        }
    elif code == 404:
        response = {
            'statusCode': 404,
            'body': json.dumps({'error': 'Unknown Resource.'}),
        }
    return response


def create_response(code: int, msg: Text) -> Dict[Text, Any]:
    return {'statusCode': code, 'body': msg}


def setup_sentry(dsn: str):
    """
    Setup the Sentry SDK and ingore console and utils loggers.

    Args:
        dsn (str): The DSN URL input from the external function.
    """
    sentry_logging = LoggingIntegration(
        level=logging.ERROR,       # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            sentry_logging,
        ]
    )
    ignore_logger('utils')
    ignore_logger('console')


def setup_dsn(event: Any) -> str:
    """Return the first dsn

    Args:
        event (Any): _description_

    Returns:
        Optional[str]: _description_
    """
    dsn: str = DEFAULT_SNOWFLAKE_ERROR_DSN
    if 'headers' not in event:
        return dsn
    headers = event['headers']
    request_body = json.loads(event['body'])
    data = request_body['data']
    ULILS_LOGGER.debug(f'Found DSN: {dsn}')

    for row_number, *args in data:
        ULILS_LOGGER.debug(f'Processing row for dsn: {row_number}.')

        process_row_params = {
            k.replace('sf-custom-', '').replace('-', '_'): format_row_dict(v, args)
            for k, v in headers.items()
            if k.startswith('sf-custom-')
        }

        return process_row_params.get('dsn', dsn)
