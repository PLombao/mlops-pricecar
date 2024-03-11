######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################
import pandas as pd
import numpy as np
from api.helpers.mlflow import download_model_from_mlflow
from api.config import MLFLOW_EXPERIMENT, MLFLOW_BUCKET_NAME
from modelbuilder.dataset import Dataset
from api.config import KEYS, FEATURES_CAT, FEATURES_NUM, TARGET, INIT_RUNID

def parse_entry(data):
    try:

        data = pd.DataFrame(data, index=[0])

        for feature in (FEATURES_CAT + FEATURES_NUM):
            if feature not in data.columns:
                data[feature] = None

        # Create dataset object
        dataset = Dataset.from_column_types(data, KEYS, FEATURES_CAT + FEATURES_NUM, TARGET)
        return dataset
    except:
        log.exception("Sthg went wrong")


class ModelManager():
    def __init__(self):
        self.runid = INIT_RUNID
        self.model = None
        self.update_model(self.runid)

    def update_model(self, runid):
        self.runid = runid
        self.model = download_model_from_mlflow(runid=self.runid, artifacts_bucket = MLFLOW_BUCKET_NAME, experiments_folder = MLFLOW_EXPERIMENT)
        self.model.base_error = 0