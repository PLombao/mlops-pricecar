
from modelbuilder.dataset import Dataset
from modelbuilder.model import Model
from modelbuilder.validation.validate import build_metrics

from api.helpers.gcp import get_df_from_bq_query
from config.config import QUERY_TRAINDATA, KEYS, FEATURES, TARGET


def load_dataset():
    """
    Load data and create dataset object
    """
    # Load data from BQ
    data = get_df_from_bq_query(QUERY_TRAINDATA)

    print(data.columns)
    print(data.head())

    # Create dataset object
    dataset = Dataset.from_column_types(data, KEYS, FEATURES, TARGET)
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
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import Pipeline

    # Dividimos las columnas en categóricas y numéricas
    categorical_columns = ['Category']
    numeric_columns = ['Engine_volume']

    # Definimos el preprocesamiento para cada tipo de columna
    # Para las categóricas usamos OneHotEncoder
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),  # Tratamiento de valores faltantes
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Para las numéricas podríamos usar un SimpleImputer para tratar valores faltantes
    # y opcionalmente un escalador como StandardScaler
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),  # Tratamiento de valores faltantes
        ('scaler', StandardScaler())])  # Escalado de características

    # Utilizamos ColumnTransformer para aplicar transformaciones por tipo de columna
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_columns),
            ('num', numeric_transformer, numeric_columns)])
    
    predictor = LinearRegression()
    
    pipeline = Pipeline([("preprocessor", preprocessor), ("predictor", predictor)])
    
    return pipeline

def get_splitter():
    """
    Get splitter for validation
    """
    from sklearn.model_selection import KFold
    splitter = KFold(5, shuffle=True)
    return splitter

def train():

    # Get data and pipeline
    dataset = load_dataset()
    pipeline = create_pipeline()

    # Create object model and fit it
    model_name = "car_price"
    model = Model(model_name, pipeline)
    model.fit(dataset)

    # Validate model and get metrics
    splitter = get_splitter()
    metrics = build_metrics(model, model.dataset, splitter)

    # Register on mlflow

    # Report model




    

   

