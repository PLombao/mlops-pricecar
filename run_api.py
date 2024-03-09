#################### Configure logging ##################
import json
import os
import logging.config
#########################################################

LOGGING_GCP = True
CLOUD_LOGGER_NAME = "py-app"

if __name__ == "__main__":

    #################### Configure logging ##################

    # LOCAL LOG
    with open('config/logging.json', 'r') as json_config:
        json_data = json.load(json_config)
        os.makedirs(os.path.dirname(json_data['handlers']['file']['filename']), exist_ok=True)
        logging.config.dictConfig(json_data)

    # GCP LOG IF PROD ENV
    if LOGGING_GCP:    
        log = logging.getLogger()

        if CLOUD_LOGGER_NAME:

            log.info(f"Running in PRODUCTION (logs being written to {CLOUD_LOGGER_NAME} GCP logger)")
            import google.cloud.logging
            from google.cloud.logging.handlers import CloudLoggingHandler
            client = google.cloud.logging.Client()
            handler = CloudLoggingHandler(client, name=CLOUD_LOGGER_NAME)
            log.addHandler(handler)
        else:
            log = logging.getLogger(__name__)
            log.error(MESSAGE_CLOUDLOGGER_NOT_FOUND)
            raise RuntimeError(MESSAGE_CLOUDLOGGER_NOT_FOUND)
    else:
        log = logging.getLogger(__name__)
        log.info("Running in DEV")

    log = logging.getLogger(__name__)

    #########################################################


    try:
        from api.api import APIService
        api = APIService(8000)
    except:
        log.exception("Error starting API")