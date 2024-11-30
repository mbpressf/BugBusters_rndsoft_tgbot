import os

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
DATADOG_API_KEY = os.environ.get('DATADOG_API_KEY')
SENTRY_DSN = os.environ.get('SENTRY_DSN')

print(ELASTICSEARCH_URL)
print(DATADOG_API_KEY)
print(SENTRY_DSN)