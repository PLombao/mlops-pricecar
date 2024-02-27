from typing import Union, Optional, Any

import mlflow
import mlflow.pyfunc

from api.helpers.storage import extract_pickle

def register_mlflow(experiment: str, python_model: mlflow.pyfunc.PythonModel, params: dict, metrics: dict, tags: dict,
               artifact_path: str = "model", conda_env: Union[str, dict, None] = None) -> Optional[str]:
    """
    Function to log models, params, metrics and tags to MLFlow. 
    Args:
        - experiment(str): experiment name where log model.
        - model (mlflow.pyfunc.PythonModel): python model with predict method.
        - params (dict): params to log. 
        - metrics (dict): metrics to log.
        - tags (dict): tags to log.
        - artifact_path (str): path to which to log the Python model.
        - conda_env (str): dict with conda env or path to a conda environment yaml file. 

    Returns: runid
    """
    # Activar el experimento. Si no existe, crea uno nuevo. 
    mlflow.set_experiment(experiment)
    with mlflow.start_run():
        try:
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.set_tags({k:v for k, v in tags.items() if v})
            if python_model is not None:
                runid = mlflow.active_run().info.run_uuid
                mlflow.pyfunc.log_model(artifact_path=artifact_path, python_model=python_model, conda_env=conda_env)
                return runid
            else:
                raise TypeError('No object python model to log in MLFlow.')
        except:
            raise Exception("Error logging model in MLFlow.")


def download_model_from_mlflow(runid:str, experimento:str, artifacts_bucket:str, experiments_folder:str) -> Any:
    """
    Downloads a MLFlow Model pickle from the storage bucket and unpickles it
    """
    source_blob_name = f'{experiments_folder}/{str(experimento)}/{runid}/artifacts/model/python_model.pkl'
    downloaded_model = extract_pickle(source_blob_name=source_blob_name, bucket_name=artifacts_bucket)
    return downloaded_model

