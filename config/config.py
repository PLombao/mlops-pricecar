

# TRAIN DATA CONFIG
QUERY_TRAINDATA = """SELECT * FROM `nifty-acolyte-415508.mlops_data.car_price_clean`"""
TARGET = "Price"
KEYS = "ID"
FEATURES_CAT = ["Manufacturer", "Model", "Category", "Leather_interior", "Fuel_type","Gear_box_type"]
FEATURES_NUM = ["Prod__year", "Engine_volume", "Mileage", "Cylinders"]