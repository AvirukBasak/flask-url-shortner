import os

APP_HOSTNAME = os.getenv('APP_HOSTNAME')
if not APP_HOSTNAME:
    raise Exception('requires APP_HOSTNAME environment variable set')
