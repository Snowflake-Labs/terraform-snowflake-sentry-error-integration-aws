# import json
# import os

# import responses
# from lambda_function import lambda_handler

# EVENT = {
#     "version": "2.0",
#     "routeKey": "ANY /{proxy+}",
#     "rawPath": "/webhook/28b78ade3e25adee904829a2c8ef61e1/83e5cd5a2a00a942e9ebc18b03d66ab6",
#     "rawQueryString": "",
#     "headers": {
#         "accept": "application/json,*/*",
#         "accept-encoding": "gzip,deflate",
#         "content-length": "5436",
#         "content-type": "application/x-www-form-urlencoded",
#         "host": "q4xlkzfswi.execute-api.ap-south-1.amazonaws.com",
#         "user-agent": "Slackbot 1.0 (+https://api.slack.com/robots)",
#         "x-amzn-trace-id": "Root=1-611f4029-77a13c6b351bcf0b5ae50a80",
#         "x-forwarded-for": "44.192.246.135",
#         "x-forwarded-port": "443",
#         "x-forwarded-proto": "https",
#         "x-slack-request-timestamp": "1629437993",
#         "x-slack-signature": "v0=634a946bcd62055fe2c48c72fbd45acd755b5462c51e2dabeb24e304bb2d1101",
#     },
#     "requestContext": {
#         "accountId": "833190679431",
#         "apiId": "q4xlkzfswi",
#         "domainName": "q4xlkzfswi.execute-api.ap-south-1.amazonaws.com",
#         "domainPrefix": "q4xlkzfswi",
#         "http": {
#             "method": "POST",
#             "path": "/webhook/a/b",
#             "protocol": "HTTP/1.1",
#             "sourceIp": "44.192.246.135",
#             "userAgent": "Slackbot 1.0 (+https://api.slack.com/robots)",
#         },
#         "requestId": "EWb2khYEhcwEPjg=",
#         "routeKey": "ANY /{proxy+}",
#         "stage": "$default",
#         "time": "20/Aug/2021:05:39:53 +0000",
#         "timeEpoch": 1629437993889,
#     },
#     "pathParameters": {"proxy": "webhook/a/b"},
#     "body": "cGF5bG9hZD0lN0IlMjJ0eXBlJTIyJTNBJTIyYmxvY2tfYWN0aW9ucyUyMiUyQyUyMnVzZXIlMjIlM0ElN0IlMjJpZCUyMiUzQSUyMlUwMUVGU1UxNlE1JTIyJTJDJTIydXNlcm5hbWUlMjIlM0ElMjJwcmFzYW50aC5rb21taW5pJTIyJTJDJTIybmFtZSUyMiUzQSUyMnByYXNhbnRoLmtvbW1pbmklMjIlMkMlMjJ0ZWFtX2lkJTIyJTNBJTIyVEJZQjhKQTBKJTIyJTdEJTJDJTIyYXBpX2FwcF9pZCUyMiUzQSUyMkEwMjNXTENDUzNFJTIyJTJDJTIydG9rZW4lMjIlM0ElMjIydGYydEhuSEV6T3pYMVRsTUpJU0JSTFolMjIlMkMlMjJjb250YWluZXIlMjIlM0ElN0IlMjJ0eXBlJTIyJTNBJTIybWVzc2FnZSUyMiUyQyUyMm1lc3NhZ2VfdHMlMjIlM0ElMjIxNjI5NDM3OTkwLjAwMDcwMCUyMiUyQyUyMmNoYW5uZWxfaWQlMjIlM0ElMjJEMDI1VDFESEc0RSUyMiUyQyUyMmlzX2VwaGVtZXJhbCUyMiUzQWZhbHNlJTdEJTJDJTIydHJpZ2dlcl9pZCUyMiUzQSUyMjI0MjUzMTU5ODQwMzIuNDA2MzgyNjIyMDE4LjdhZDJjNjRhNTY4ZTk1Njk2NzNiMWU3Y2NjZGMwMTZhJTIyJTJDJTIydGVhbSUyMiUzQSU3QiUyMmlkJTIyJTNBJTIyVEJZQjhKQTBKJTIyJTJDJTIyZG9tYWluJTIyJTNBJTIyc25vd2ZsYWtlLXNlY3VyaXR5JTIyJTdEJTJDJTIyZW50ZXJwcmlzZSUyMiUzQW51bGwlMkMlMjJpc19lbnRlcnByaXNlX2luc3RhbGwlMjIlM0FmYWxzZSUyQyUyMmNoYW5uZWwlMjIlM0ElN0IlMjJpZCUyMiUzQSUyMkQwMjVUMURIRzRFJTIyJTJDJTIybmFtZSUyMiUzQSUyMmRpcmVjdG1lc3NhZ2UlMjIlN0QlMkMlMjJtZXNzYWdlJTIyJTNBJTdCJTIyYm90X2lkJTIyJTNBJTIyQjAyM0hOOVA0TlMlMjIlMkMlMjJ0eXBlJTIyJTNBJTIybWVzc2FnZSUyMiUyQyUyMnRleHQlMjIlM0ElMjJUaGlzK2NvbnRlbnQrY2FuJTI3dCtiZStkaXNwbGF5ZWQuJTIyJTJDJTIydXNlciUyMiUzQSUyMlUwMjRFOVpEVkxHJTIyJTJDJTIydHMlMjIlM0ElMjIxNjI5NDM3OTkwLjAwMDcwMCUyMiUyQyUyMnRlYW0lMjIlM0ElMjJUQllCOEpBMEolMjIlMkMlMjJibG9ja3MlMjIlM0ElNUIlN0IlMjJ0eXBlJTIyJTNBJTIyaGVhZGVyJTIyJTJDJTIyYmxvY2tfaWQlMjIlM0ElMjJoSXU4RCUyMiUyQyUyMnRleHQlMjIlM0ElN0IlMjJ0eXBlJTIyJTNBJTIycGxhaW5fdGV4dCUyMiUyQyUyMnRleHQlMjIlM0ElMjJTZWN1cml0eStBbGVydCUzQStQcm9kdWN0aW9uK0ppcmElNUMlMkZTbGFjaytUaW5lcyt0ZXN0JTIyJTJDJTIyZW1vamklMjIlM0F0cnVlJTdEJTdEJTJDJTdCJTIydHlwZSUyMiUzQSUyMnNlY3Rpb24lMjIlMkMlMjJibG9ja19pZCUyMiUzQSUyMiU1QyUyRktuYUslMjIlMkMlMjJ0ZXh0JTIyJTNBJTdCJTIydHlwZSUyMiUzQSUyMm1ya2R3biUyMiUyQyUyMnRleHQlMjIlM0ElMjIlMkFEZXNjcmlwdGlvbiUyQSUzQStUaGVyZSt3YXMrYStzdXNwaWNpb3VzK3N1ZG8rY29tbWFuZCtyYW4rb24reW91citob3N0LitEbyt5b3UrcmVjb2duaXplK3RoZStiZWxvdytpbmZvcm1hdGlvbiUzRiU1Q24lNUNuJTJBJTJBZGV0YWlscytjcmFmdGVkK2luK2VhY2grcGxheWJvb2slMkElMkElNUNuJTVDbiUyQUluY2lkZW50K0lEJTJBJTNBK1RUQlQtMSUyMiUyQyUyMnZlcmJhdGltJTIyJTNBZmFsc2UlN0QlMkMlMjJhY2Nlc3NvcnklMjIlM0ElN0IlMjJ0eXBlJTIyJTNBJTIyaW1hZ2UlMjIlMkMlMjJpbWFnZV91cmwlMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRnd3dy5rbGlwZm9saW8uY29tJTVDJTJGc2l0ZXMlNUMlMkZkZWZhdWx0JTVDJTJGZmlsZXMlNUMlMkZpbnRlZ3JhdGlvbnMlNUMlMkZzbm93Zmxha2UucG5nJTIyJTJDJTIyYWx0X3RleHQlMjIlM0ElMjJsb2dvJTIyJTdEJTdEJTJDJTdCJTIydHlwZSUyMiUzQSUyMmNvbnRleHQlMjIlMkMlMjJibG9ja19pZCUyMiUzQSUyMjNhJTNEcSUyMiUyQyUyMmVsZW1lbnRzJTIyJTNBJTVCJTdCJTIydHlwZSUyMiUzQSUyMm1ya2R3biUyMiUyQyUyMnRleHQlMjIlM0ElMjIlNUN1MjIxOSslMkFBV1MrYWNjb3VudCUyQSUzQStzZmMtc2VjdXJpdHklNUNuJTVDdTIyMTkrJTJBSUFNK2FjY291bnQlMkElM0ErYXdpbmRsZSUyMiUyQyUyMnZlcmJhdGltJTIyJTNBZmFsc2UlN0QlNUQlN0QlMkMlN0IlMjJ0eXBlJTIyJTNBJTIyYWN0aW9ucyUyMiUyQyUyMmJsb2NrX2lkJTIyJTNBJTIyc2VuZF9tZXNzYWdlX3RvX3VzZXIlMjIlMkMlMjJlbGVtZW50cyUyMiUzQSU1QiU3QiUyMnR5cGUlMjIlM0ElMjJidXR0b24lMjIlMkMlMjJhY3Rpb25faWQlMjIlM0ElMjJjb25maXJtJTIyJTJDJTIydGV4dCUyMiUzQSU3QiUyMnR5cGUlMjIlM0ElMjJwbGFpbl90ZXh0JTIyJTJDJTIydGV4dCUyMiUzQSUyMkkrcmVjb2duaXplK3RoaXMlMjIlMkMlMjJlbW9qaSUyMiUzQXRydWUlN0QlMkMlMjJzdHlsZSUyMiUzQSUyMnByaW1hcnklMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMiUyM2V2ZW50X2lkJTVDJTIyJTNBbnVsbCUyQyU1QyUyMiUyM2FnZW50X2lkJTVDJTIyJTNBMzUwJTJDJTVDJTIyYm9keSU1QyUyMiUzQSU3QiU1QyUyMmVtYWlsJTVDJTIyJTNBJTVDJTIycHJhc2FudGgua29tbWluaSU0MHNub3dmbGFrZS5jb20lNUMlMjIlMkMlNUMlMjJtZXNzYWdlJTVDJTIyJTNBJTVDJTIyVGhlcmUrd2FzK2Erc3VzcGljaW91cytzdWRvK2NvbW1hbmQrcmFuK29uK3lvdXIraG9zdC4rRG8reW91K3JlY29nbml6ZSt0aGUrYmVsb3craW5mb3JtYXRpb24lM0YlNUMlNUNuJTVDJTVDbiUyQSUyQWRldGFpbHMrY3JhZnRlZCtpbitlYWNoK3BsYXlib29rJTJBJTJBJTVDJTIyJTJDJTVDJTIyaW5jaWRlbnRfaWQlNUMlMjIlM0ElNUMlMjJUVEJULTElNUMlMjIlMkMlNUMlMjJpbmNpZGVudF90eXBlJTVDJTIyJTNBJTVDJTIyUHJvZHVjdGlvbitKaXJhJTVDJTJGU2xhY2srVGluZXMrdGVzdCU1QyUyMiUyQyU1QyUyMmZvb3RlciU1QyUyMiUzQSU1QiU3QiU1QyUyMmtleSU1QyUyMiUzQSU1QyUyMkFXUythY2NvdW50JTVDJTIyJTJDJTVDJTIydmFsdWUlNUMlMjIlM0ElNUMlMjJzZmMtc2VjdXJpdHklNUMlMjIlN0QlMkMlN0IlNUMlMjJrZXklNUMlMjIlM0ElNUMlMjJJQU0rYWNjb3VudCU1QyUyMiUyQyU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyYXdpbmRsZSU1QyUyMiU3RCU1RCUyQyU1QyUyMnJlc3BvbnNlX3RpbWVfaG91cnMlNUMlMjIlM0ElNUMlMjI4JTVDJTIyJTdEJTdEJTIyJTdEJTJDJTdCJTIydHlwZSUyMiUzQSUyMmJ1dHRvbiUyMiUyQyUyMmFjdGlvbl9pZCUyMiUzQSUyMmRlbnklMjIlMkMlMjJ0ZXh0JTIyJTNBJTdCJTIydHlwZSUyMiUzQSUyMnBsYWluX3RleHQlMjIlMkMlMjJ0ZXh0JTIyJTNBJTIySStkb24lMjd0K3JlY29nbml6ZSt0aGlzJTIyJTJDJTIyZW1vamklMjIlM0F0cnVlJTdEJTJDJTIyc3R5bGUlMjIlM0ElMjJkYW5nZXIlMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMiUyM2V2ZW50X2lkJTVDJTIyJTNBbnVsbCUyQyU1QyUyMiUyM2FnZW50X2lkJTVDJTIyJTNBMzUwJTJDJTVDJTIyYm9keSU1QyUyMiUzQSU3QiU1QyUyMmVtYWlsJTVDJTIyJTNBJTVDJTIycHJhc2FudGgua29tbWluaSU0MHNub3dmbGFrZS5jb20lNUMlMjIlMkMlNUMlMjJtZXNzYWdlJTVDJTIyJTNBJTVDJTIyVGhlcmUrd2FzK2Erc3VzcGljaW91cytzdWRvK2NvbW1hbmQrcmFuK29uK3lvdXIraG9zdC4rRG8reW91K3JlY29nbml6ZSt0aGUrYmVsb3craW5mb3JtYXRpb24lM0YlNUMlNUNuJTVDJTVDbiUyQSUyQWRldGFpbHMrY3JhZnRlZCtpbitlYWNoK3BsYXlib29rJTJBJTJBJTVDJTIyJTJDJTVDJTIyaW5jaWRlbnRfaWQlNUMlMjIlM0ElNUMlMjJUVEJULTElNUMlMjIlMkMlNUMlMjJpbmNpZGVudF90eXBlJTVDJTIyJTNBJTVDJTIyUHJvZHVjdGlvbitKaXJhJTVDJTJGU2xhY2srVGluZXMrdGVzdCU1QyUyMiUyQyU1QyUyMmZvb3RlciU1QyUyMiUzQSU1QiU3QiU1QyUyMmtleSU1QyUyMiUzQSU1QyUyMkFXUythY2NvdW50JTVDJTIyJTJDJTVDJTIydmFsdWUlNUMlMjIlM0ElNUMlMjJzZmMtc2VjdXJpdHklNUMlMjIlN0QlMkMlN0IlNUMlMjJrZXklNUMlMjIlM0ElNUMlMjJJQU0rYWNjb3VudCU1QyUyMiUyQyU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyYXdpbmRsZSU1QyUyMiU3RCU1RCUyQyU1QyUyMnJlc3BvbnNlX3RpbWVfaG91cnMlNUMlMjIlM0ElNUMlMjI4JTVDJTIyJTdEJTdEJTIyJTdEJTVEJTdEJTVEJTdEJTJDJTIyc3RhdGUlMjIlM0ElN0IlMjJ2YWx1ZXMlMjIlM0ElN0IlN0QlN0QlMkMlMjJyZXNwb25zZV91cmwlMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmhvb2tzLnNsYWNrLmNvbSU1QyUyRmFjdGlvbnMlNUMlMkZUQllCOEpBMEolNUMlMkYyMzk0OTQ0MDgyNTY2JTVDJTJGRkJsbDcyZHNKaTNBaENFMWU5dUJ1N29wJTIyJTJDJTIyYWN0aW9ucyUyMiUzQSU1QiU3QiUyMmFjdGlvbl9pZCUyMiUzQSUyMmNvbmZpcm0lMjIlMkMlMjJibG9ja19pZCUyMiUzQSUyMnNlbmRfbWVzc2FnZV90b191c2VyJTIyJTJDJTIydGV4dCUyMiUzQSU3QiUyMnR5cGUlMjIlM0ElMjJwbGFpbl90ZXh0JTIyJTJDJTIydGV4dCUyMiUzQSUyMkkrcmVjb2duaXplK3RoaXMlMjIlMkMlMjJlbW9qaSUyMiUzQXRydWUlN0QlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMiUyM2V2ZW50X2lkJTVDJTIyJTNBbnVsbCUyQyU1QyUyMiUyM2FnZW50X2lkJTVDJTIyJTNBMzUwJTJDJTVDJTIyYm9keSU1QyUyMiUzQSU3QiU1QyUyMmVtYWlsJTVDJTIyJTNBJTVDJTIycHJhc2FudGgua29tbWluaSU0MHNub3dmbGFrZS5jb20lNUMlMjIlMkMlNUMlMjJtZXNzYWdlJTVDJTIyJTNBJTVDJTIyVGhlcmUrd2FzK2Erc3VzcGljaW91cytzdWRvK2NvbW1hbmQrcmFuK29uK3lvdXIraG9zdC4rRG8reW91K3JlY29nbml6ZSt0aGUrYmVsb3craW5mb3JtYXRpb24lM0YlNUMlNUNuJTVDJTVDbiUyQSUyQWRldGFpbHMrY3JhZnRlZCtpbitlYWNoK3BsYXlib29rJTJBJTJBJTVDJTIyJTJDJTVDJTIyaW5jaWRlbnRfaWQlNUMlMjIlM0ElNUMlMjJUVEJULTElNUMlMjIlMkMlNUMlMjJpbmNpZGVudF90eXBlJTVDJTIyJTNBJTVDJTIyUHJvZHVjdGlvbitKaXJhJTVDJTJGU2xhY2srVGluZXMrdGVzdCU1QyUyMiUyQyU1QyUyMmZvb3RlciU1QyUyMiUzQSU1QiU3QiU1QyUyMmtleSU1QyUyMiUzQSU1QyUyMkFXUythY2NvdW50JTVDJTIyJTJDJTVDJTIydmFsdWUlNUMlMjIlM0ElNUMlMjJzZmMtc2VjdXJpdHklNUMlMjIlN0QlMkMlN0IlNUMlMjJrZXklNUMlMjIlM0ElNUMlMjJJQU0rYWNjb3VudCU1QyUyMiUyQyU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyYXdpbmRsZSU1QyUyMiU3RCU1RCUyQyU1QyUyMnJlc3BvbnNlX3RpbWVfaG91cnMlNUMlMjIlM0ElNUMlMjI4JTVDJTIyJTdEJTdEJTIyJTJDJTIyc3R5bGUlMjIlM0ElMjJwcmltYXJ5JTIyJTJDJTIydHlwZSUyMiUzQSUyMmJ1dHRvbiUyMiUyQyUyMmFjdGlvbl90cyUyMiUzQSUyMjE2Mjk0Mzc5OTMuMjI5OTcxJTIyJTdEJTVEJTdE",
#     "isBase64Encoded": True,
# }


# @responses.activate
# def test_good_url():
#     TEST_URL = (
#         'https://tines-test-load-balancer-1234.ap-west-4.elb.amazonaws.com/abc/xyz'
#     )
#     BODY = {"result": "Some useful result."}
#     SHOULD_MATCH = {
#         'statusCode': 404,
#         'body': json.dumps(BODY),
#     }

#     responses.add(
#         responses.Response(
#             method=responses.POST,
#             url=TEST_URL,
#             json=BODY,
#             status=404,
#             match_querystring=True,
#         )
#     )
#     assert lambda_handler(EVENT, None) == SHOULD_MATCH


# def test_bad_url():
#     EVENT.update({"rawPath": "/slack-notwebhook"})
#     TEST_URL = (
#         'https://tines-test-load-balancer-1234.ap-west-4.elb.amazonaws.com/abc/xyz'
#     )
#     ERROR_BODY = {"error": "Unknown Resource."}
#     SHOULD_MATCH = {
#         'statusCode': 404,
#         'body': json.dumps(ERROR_BODY),
#     }
#     assert lambda_handler(EVENT, None) == SHOULD_MATCH
