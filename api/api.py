######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

import uvicorn
from fastapi import FastAPI, BackgroundTasks

from api.routers import router


class APIService:
    """API to manage model inference, retraining and deploy."""
    def __init__(self, port):
        log.info("Starting APIService")
        try:
            self.config()
            self._run(port)
        except:
            log.exception("Error running API")

    def _run(self, port):
        try:
            uvicorn.run(self.app, host="0.0.0.0", port=port)
        except:
            log.exception("Error running uvicorn")

    def config(self):
        self.app = FastAPI()
        self.app.include_router(router)
