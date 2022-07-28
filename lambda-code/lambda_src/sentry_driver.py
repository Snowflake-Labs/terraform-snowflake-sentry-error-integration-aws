import logging
import os
from datetime import date, timedelta
from typing import Any

import sentry_sdk
from sentry_sdk import push_scope

from .log import setup_logger

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL')
AWS_REGION = os.environ.get('AWS_REGION')

CONSOLE_LOGGER = setup_logger(
    'console',
    logging.INFO if LOGGING_LEVEL in {None, 'INFO', 'info'}
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


def process_message(message: Any) -> Any:
    CONSOLE_LOGGER.debug(f"From SNS: {message}")

    pipe_full_name = message['pipeName']
    database, schema_and_pipe = pipe_full_name.split(".", 1)
    schema, pipe_name = schema_and_pipe.split(".", 1)

    history_type = 'copy'
    error_msg = message['messages'][0]['firstError'] if message['messages'][0] else 'PIPE ERROR'
    timestamp = message['timestamp']
    account_name = message['accountName'].lower()
    date_today = str(date.today())
    date_1_week_back = str(date.today() - timedelta(days=7))

    pipe_error_history_url: str = (
        f'https://app.snowflake.com/{AWS_REGION}/{account_name}/compute/history/copies?'
        + 'type=relative&relative={"tense":"past","value":7,"unit":"day","excludePartial":false,"exclusionSize":"day","exclusionSizeParam":""}'
        + f'&startDate={date_today}&endDate={date_1_week_back}'
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
