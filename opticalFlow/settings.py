import os

# Api configuration----------------------------------------------------------------------------------------------------
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', '8000')
RELOAD = os.environ.get('RELOAD', False)  # for production default is False
# SSL is for SSL usage for https webserver configuration. If None - web server will be in http mnode
SSL_KEYFILE = os.environ.get('SSL_KEYFILE', None)
SSL_CERTFILE = os.environ.get('SSL_CERTFILE', None)
SSL_KEYFILE_PASSWORD = os.environ.get('SSL_KEYFILE_PASSWORD', None)

# The below commented segment with BASE_DIR only for the logging in a file.
# If some kinda monitoring stack like ELK will be used - just configure filebeat 
# for taking stdout from docker and output in kibana and remove file logging.
# Also configure docker for log rotation like this in /etc/docker/daemon.json:
# {"log-driver": "json-file",
#  "log-opts": {
#   "max-size": "5m",
#   "max-file": "3"
#  }
# }

# BASE_DIR = os.path.abspath(os.getcwd())
# LOG_DIR = BASE_DIR + '/log'
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(name)s:%(levelname)s] %(module)s:%(funcName)s:%(lineno)d %(message)s'
        },
        'json': {
            "()": "logging_formatter.JsonFormatter"
        }
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'console_info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'console_json': {
            'level': 'DEBUG',
            'class': 'logger.StreamHandler',
            'formatter': 'json'
        },
        'console_info_json': {
            'level': 'INFO',
            'class': 'logger.StreamHandler',
            'formatter': 'json'
        }
        # Also file logging can be added as mentioned below - ibnfo about LOG_DIR is above
        # 'file_basic': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': LOG_DIR + '/api_optic_flow_demo.log',
        #     'formatter': 'json'
        # }
    }
}

# CV configuration-----------------------------------------------------------------------------------------------------
# Use later to store here all needed configuration for different cv methods
# and also default values for cv methods
