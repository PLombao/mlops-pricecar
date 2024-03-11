

# TRAIN DATA CONFIG
QUERY_TRAINDATA = """SELECT * FROM `nifty-acolyte-415508.mlops_data.car_price_clean`"""
TARGET = "Price"
KEYS = ["ID"]
FEATURES_CAT = ["Manufacturer", "Category", "Leather_interior", "Fuel_type","Gear_box_type"]
FEATURES_NUM = ["Prod__year", "Engine_volume", "Mileage", "Cylinders"]


MLFLOW_EXPERIMENT = "307835850722356415"
MLFLOW_BUCKET_NAME = "mlflow-plv"
INIT_RUNID = "1a1c3087a95e4400af64b6b45f1f6220"