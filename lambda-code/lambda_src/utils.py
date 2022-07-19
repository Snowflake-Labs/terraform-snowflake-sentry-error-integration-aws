import re
import json
import logging
from typing import Any, Dict, Text

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from .log import setup_logger

ULILS_LOGGER = setup_logger('utils', logging.DEBUG)


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
