

# TRAIN DATA CONFIG
QUERY_TRAINDATA = """SELECT * FROM `nifty-acolyte-415508.mlops_data.car_price_full`"""
FEATURES =  ["Manufacturer", "Model", "Prod__year", "Category", "Leather_interior", "Fuel_type", "Engine_volume", "Mileage", "Cylinders","Gear_box_type"]
TARGET = "Price"
KEYS = "ID"