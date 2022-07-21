import os
import logging

import sentry_sdk
from sentry_sdk import push_scope

from .log import setup_logger

logging_level = os.environ.get('LOGGING_LEVEL')
CONSOLE_LOGGER = setup_logger(
    'console',
    logging.INFO if logging_level in {None, 'INFO', 'info'}
    else logging.DEBUG
)
SENTRY_DRIVER_LOGGER = setup_logger(
    'sentry_driver', logging.INFO
)


def process_row(
    name: str,
    history_type: str,
    error: str,
    ts: str,
    history_url: str,
    **kwargs,
):
    """
    Each row is sent to Sentry via the SENTRY_DRIVER_LOGGER.

    Args:
        name (str): The object name.
        history_type (str): pipe or task or query.
        error (str): The actual error message.
        ts (str): The timestamp of the error.
        history_url (str): URL of the erroring object in history.
    """
    CONSOLE_LOGGER.info(f'sentry_logger driver invoked.')

    try:
        with push_scope() as scope:
            scope.set_extra('history_url', history_url)
            sentry_sdk.set_tag(
                (
                    'PIPE_NAME'
                    if history_type in ('copy', 'COPY')
                    else 'TASK_NAME'
                    if history_type in ('task', 'TASK')
                    else 'QUERY_ID'
                ),
                name
            )
            sentry_sdk.set_tag('error', error)
            sentry_sdk.set_tag('error_time', ts)
            sentry_sdk.set_tag('history_type', history_type)
            SENTRY_DRIVER_LOGGER.exception(error)
    except Exception as e:
        return f'Unable to capture {name} error at {ts}.'
    else:
        return f'Captured {name} error at {ts}.'
