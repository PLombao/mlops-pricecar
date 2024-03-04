######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

from fastapi import APIRouter, Response, status

from .models import InferRequest, InferResponse

router = APIRouter()

@router.get('/')
def index():
    return "Welcome to ServiceAPI"

@router.get('/train')
def index():
  # Launch training on another Thread

  return "Trained completed"

{runid}
@router.post('/deploy')
def index():
  runid = payload.runid

  # Deploy model
  
  return "Model deployed"


# MAIN METHOD ALIGN REQUEST {linea, timestamp, variables}
@router.post('/predict', response_model=InferResponse)
def index(payload: InferRequest):
    # TODO: CHANGE THIS
    # Parse entry
    linea , asked_timestamp, variables = payload.linea, payload.timestamp, payload.variables
    
    log.info(f"Received request to align for line {linea} on {asked_timestamp}. Vars: {variables}")
    
    # Call backend
    response = router.requester.get_aligned_data(linea, asked_timestamp, variables)

    response = response.serialize()

    log.info(f"Response dict: {response}")

    return response



import random
@router.get("/comoestanlosmaquinas")
def index():
    states = ["caimán", "crack", "esturión", "jefe", "gamo", "capibara", 
              "miura", "mastodonte","fiera", "figura", "titan", "diplodocus","triceraptors"]
    return {"state": f"estamos bien, {states[random.randint(0,12)]}"}
