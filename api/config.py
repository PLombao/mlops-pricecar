

# TRAIN DATA CONFIG
QUERY_TRAINDATA = """SELECT * FROM `nifty-acolyte-415508.mlops_data.car_price_clean`"""
TARGET = "Price"
KEYS = ["ID"]
FEATURES_CAT = ["Manufacturer", "Category", "Leather_interior", "Fuel_type","Gear_box_type"]
FEATURES_NUM = ["Prod__year", "Engine_volume", "Mileage", "Cylinders"]


MLFLOW_EXPERIMENT = "196847260286025580"
MLFLOW_BUCKET_NAME = "mlflow-plv"
INIT_RUNID = "4690c5c7d01a4f7689e7e34c4afe1f39"