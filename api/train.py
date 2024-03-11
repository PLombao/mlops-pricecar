######## HEADER TO CONFIGURE LOGS ########
import logging
log = logging.getLogger(__name__)
##########################################

import time
from modelbuilder.dataset import Dataset
from modelbuilder.model import Model
from modelbuilder.validation.validate import build_metrics

from api.helpers.bq import get_df_from_bq_query
from api.helpers.mlflow import register_mlflow
from api.config import QUERY_TRAINDATA, KEYS, FEATURES_CAT, FEATURES_NUM, TARGET


def load_dataset():
    """
    Load data and create dataset object
    """
    # Load data from BQ
    data = get_df_from_bq_query(QUERY_TRAINDATA)

    print(data.columns)
    print(data.head())

    # Create dataset object
    dataset = Dataset.from_column_types(data, KEYS, FEATURES_CAT + FEATURES_NUM, TARGET)
    return dataset

def create_pipeline():
    """
    Create pipeline for train
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVR
    from sklearn.ensemble import GradientBoostingRegressor, VotingRegressor
    from sklearn.pipeline import Pipeline

    # Dividimos las columnas en categóricas y numéricas
    categorical_columns = FEATURES_CAT
    numeric_columns = FEATURES_NUM

    # Definimos el preprocesamiento para cada tipo de columna
    # Para las categóricas usamos OneHotEncoder
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),  # Tratamiento de missings
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Para las numéricas podríamos usar un SimpleImputer para tratar valores faltantes
    # y para normalizar un StandardScaler
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),  # Tratamiento de missings
        ('scaler', StandardScaler())])  # Escalado de características

    # Utilizamos ColumnTransformer para aplicar transformaciones por tipo de columna
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_columns),
            ('num', numeric_transformer, numeric_columns)])
    
    # Predictor: ensemble con GB y SVR
    predictor_params_SVR = {"epsilon":0.025}
    predictor_params_GB = {"n_estimators": 100}

    ensemble_models = [("SVR", SVR(**predictor_params_SVR)), ("GB", GradientBoostingRegressor(**predictor_params_GB))]
    predictor = VotingRegressor(ensemble_models)

    pipeline = Pipeline([("preprocessor", preprocessor), ("predictor", predictor)])
    
    return pipeline

def get_ci():
    """"
    Get Confidence Interval
    """
    from api.confidence_interval import ConfidenceIntervalEnsemble
    ci = ConfidenceIntervalEnsemble()
    return ci

def get_splitter():
    """
    Get splitter for validation
    """
    from sklearn.model_selection import KFold
    splitter = KFold(2, shuffle=True)
    return splitter

def train():
    log.info("Starting train...")
    t0 = time.time()
    try:
        # Get data, pipeline and ci
        dataset = load_dataset()
        pipeline = create_pipeline()
        ci = get_ci()
        log.info("Loaded dataset and pipeline")

        # Create object model and fit it
        model_name = "car_price"
        model = Model(model_name, pipeline, ci)
        model.fit(dataset)
        log.info("Model fitted.")

        # Validate model and get metrics
        splitter = get_splitter()
        metrics = build_metrics(model, model.dataset, splitter)
        log.info("Model validated.")

        # Register on mlflow
        import os
        os.environ["MLFLOW_TRACKING_URI"]="http://host.docker.internal:5000"
        runid = register_mlflow(experiment = model_name, python_model = model, metrics = metrics, params={}, tags = {})
        log.info(f"Model registered in MLFLOW with runid: {runid}.")
        log.info(f"Training time: {time.time() - t0}s")
        return runid
    except:
        log.exception("An error ocurred while training.")
    




    

   

