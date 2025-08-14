import os

import dotenv

class AuthSettings:
    SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    ALGORITHM = os.getenv('AUTH_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))


AUTHSETTINGS = AuthSettings
