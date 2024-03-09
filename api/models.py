######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

from pydantic import BaseModel
from typing import Dict, Union

DictSerie = Dict[str, Union[float, str]]

class DeployRequest(BaseModel):
    runid: str

class InferRequest(BaseModel):
    features: DictSerie

class InferResponse(BaseModel):
    state: str
    prediction: DictSerie