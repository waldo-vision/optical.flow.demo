import uvicorn
from settings import RELOAD, SSL_CERTFILE, SSL_KEYFILE, SSL_KEYFILE_PASSWORD

import settings
from api import app

if __name__ == '__main__':
    uvicorn.run(app=app,
                host=settings.HOST,
                port=int(settings.PORT),
                reload=settings.RELOAD, # for production default is False
                # log_config=settings.LOGGING # You can add custom logging configuration here
                ssl_keyfile=settings.SSL_KEYFILE,
                ssl_certfile=settings.SSL_CERTFILE,
                ssl_keyfile_password=settings.SSL_KEYFILE_PASSWORD)