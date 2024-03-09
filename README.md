# mlops-pricecar
MLOps system for price car prediction



## DEPLOY

curl http://localhost:8000/deploy -H "Content-Type: application/json" -d '{"runid":"0c909193a2374489aba41d5a27c90ea5"}'


## PREDICT

curl http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features":{"ID":"55816599", "Manufacturer":"BMW", "Model":"X5"}}'

ID,Price,Manufacturer,Model,Prod__year,Category,Leather_interior,Fuel_type,Engine_volume,Mileage,Cylinders,Gear_box_type