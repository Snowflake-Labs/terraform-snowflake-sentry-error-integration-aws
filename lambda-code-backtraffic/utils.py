import base64
import hashlib
import hmac
import json
import logging
import sys
import time
from typing import Dict, Text

import boto3

logging.basicConfig(stream=sys.stdout)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def get_secrets(secret_name: Text) -> Text:
    """Gets values from secrets manager

    Args:
        secret_name (Text): The secrets name

    Returns:
        A string of the secrets in secrets manager. You will need to jsonify it if its in json.
    """
    client = boto3.client(service_name='secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return get_secret_value_response['SecretString']


def verify_request(
    slack_signature: Text,
    slack_timestamp: Text,
    slack_event_body: Text,
    app_signing_secret: Text,
) -> bool:
    """
    Does the header sent in the request match the secret token.
    If it doesn't it may be an insecure request from someone trying to pose as your
    application. You can read more about the url-verification and why this is necessary
    here https://api.slack.com/docs/verifying-requests-from-slack

    Args:
        app_signing_secret (Text): The apps local signing secret that is given by slack to compare with formulated.
        slack_signature (Text): The header of the http_request from slack X-Slack-Signature
        slack_timestamp (Text): The header of the http_request from slack X-Slack-Request-Timestamp
        slack_event_body (Text): The slack event body that must be formulated as a string

    Returns:
        A boolean. If True the request was valid if False request was not valid.
    """
    if abs(time.time() - float(slack_timestamp)) > 60 * 5:
        # The request is older then 5 minutes
        LOG.warning(
            f'Request verification failed. Timestamp was over 5 mins old for the request'
        )
        return False
    sig_basestring = f'v0:{slack_timestamp}:{slack_event_body}'.encode('utf-8')
    slack_signing_secret = bytes(app_signing_secret, 'utf-8')
    my_signature = (
        'v0='
        + hmac.new(slack_signing_secret, sig_basestring, hashlib.sha256).hexdigest()
    )
    if hmac.compare_digest(my_signature, slack_signature):
        return True
    else:
        LOG.warning(
            f'Verification failed. my_signature: {my_signature} slack_signature: {slack_signature}'
        )
        return False


def extract_from_b64(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


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
