import json
from json.decoder import JSONDecodeError
from typing import Dict, Text

import requests
from utils import (
    LOG,
    WEBHOOKS,
    error_response,
    extract_from_b64,
    get_secrets,
    is_supported,
    verify_request,
)


def lambda_handler(event, context):
    headers: dict = event['headers']
    body: dict = event['body']

    r = requests.post(
        tines_url,
        headers=headers,
        data=body.encode('utf-8'),
    )

    try:
        body = r.content
    except JSONDecodeError:
        body = r.text

    return {'statusCode': r.status_code, 'body': body}
