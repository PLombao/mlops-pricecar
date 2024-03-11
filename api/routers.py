######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

import threading
import time
from fastapi import APIRouter
from .models import InferRequest, InferResponse, DeployRequest
from .train import train
from .infer import ModelManager, parse_entry
from .helpers.bq import insert_row

router = APIRouter()
modelmanager = ModelManager()

@router.get('/')
def index():
    return "Welcome to ServiceAPI"

@router.get('/train')
def index():
  # Launch training on another Thread
  train_thread = threading.Thread(target=train)

  train_thread.start()

  return "Train request received"

@router.post('/deploy')
def index(payload: DeployRequest):
  runid = payload.runid

  # Deploy model
  modelmanager.update_model(runid)
  
  return f"Model {runid} deployed"


# MAIN METHOD ALIGN REQUEST {linea, timestamp, variables}
@router.post('/predict', response_model=InferResponse)
def index(payload: InferRequest):
    log.info(f"Received request to predict.")
    t0 = time.time()
    # Parse entry and build dataset
    features = payload.features
    log.info(features)

    # Parse dataset
    dataset = parse_entry(features)

    try:
      # Call backend model
      dataset = modelmanager.model.predict(None, dataset)
 
      # Insert on BQ
      insert_row(dataset.data)

      # Parse response for API
      response = dataset.data[["ID","prediction", "ci_min","ci_max"]].to_dict("records")[0]
      log.info(response)
      log.info(f"Inference time: {time.time() - t0}s")
      return {"state": "OK", "prediction": response}
    except:
       log.exception("Ups")


import random
@router.get("/comoestanlosmaquinas")
def index():
    states = ["caimán", "crack", "esturión", "jefe", "gamo", "capibara", 
              "miura", "mastodonte","fiera", "figura", "titan", "diplodocus","triceraptors"]
    return {"state": f"estamos bien, {states[random.randint(0,12)]}",
            "model_deployed":modelmanager.runid}
