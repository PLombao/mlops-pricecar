######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

from pydantic import BaseModel

class InferRequest(BaseModel):
    linea: str

class InferResponse(BaseModel):
    asked_timestamp: str