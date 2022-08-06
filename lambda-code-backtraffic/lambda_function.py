import json
import os
from json.decoder import JSONDecodeError
from typing import Dict, Text, List

import requests
from utils import (LOG, error_response, extract_from_b64, get_secrets,
                   verify_request)

SENTRY_HOSTNAME = os.environ.get('SENTRY_HOSTNAME')

SLACK_SECRET_ARN = os.environ.get('SLACK_SECRET_ARN')
JIRA_SECRET_ARN = os.environ.get('JIRA_SECRET_ARN')

ALLOWED_SLACK_URLS: List = [
    '/extensions/slack/event/',
    '/extensions/slack/commands/',
    '/extensions/slack/action/',
    '/extensions/slack/options-load/',
]
ALLOWED_JIRA_URLS: List = []


def lambda_handler(event, context):
    headers: Dict = event['headers']
    body: Dict = event['body']
    raw_path = event.get('rawPath')
    LOG.info(f'rawPath is {raw_path}.')

    if event['isBase64Encoded']:
        body: str = extract_from_b64(body)

    slack_signature: str = headers.get('x-slack-signature')
    slack_request_ts: str = headers.get('x-slack-request-timestamp')

    # Slack Request
    if slack_signature and slack_request_ts:
        if raw_path not in ALLOWED_SLACK_URLS:
            LOG.warning('Unsupported path.')
            return error_response(404)

        url = f'https://{SENTRY_HOSTNAME}{raw_path}'
        LOG.info(f'Using Sentry URL: {url}')

        sentry_secrets: Dict = json.loads(get_secrets(SLACK_SECRET_ARN))
        if type(sentry_secrets) is not dict:
            raise TypeError('Secrets response must be a dictionary.')

        signing_secret: str = sentry_secrets.get('SENTRY_SLACK_SIGNING_SECRET')

        if not verify_request(
            slack_signature,
            slack_request_ts,
            body,
            signing_secret,
        ):
            LOG.warning('Signature Verification failed.')
            return error_response(403)

        LOG.info('Verification successful. Forwarding request.')
    # JIRA Request
    # elif 'jira-header' in headers:
        # Grab secrets for the application.
        # jira_secrets: Dict = json.loads(get_secrets(JIRA_SECRET_NAME))
        # if type(sentry_secrets) is not dict:
            # raise TypeError('Secrets response must be a dictionary.')
    else:
        LOG.warning('Unsupported path.')
        return error_response(404)
    
    LOG.info('Forwarding request.')
    r = requests.post(
        url,
        headers=headers,
        data=body.encode('utf-8'),
    )
    LOG.info('Received response.')

    try:
        body = r.content
    except JSONDecodeError:
        body = r.text

    print(r.headers)
    return {'statusCode': r.status_code, 'body': body}

