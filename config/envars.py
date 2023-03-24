if __name__ == '__main__':
    exit(1)

import os

APP_HOSTNAME = os.getenv('APP_HOSTNAME')
if not APP_HOSTNAME:
    raise Exception('requires APP_HOSTNAME environment variable set')
