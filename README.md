# mlops-pricecar
MLOps system for price car prediction



## DEPLOY

curl http://localhost:8000/deploy -H "Content-Type: application/json" -d '{"runid":"a15d82c5ce2b4ce287aa9ffa0b725b4a"}'


## PREDICT

curl http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features":{"ID":55816599, "Manufacturer":"BMW", "Model":"X5"}}'

ID,Price,Manufacturer,Model,Prod__year,Category,Leather_interior,Fuel_type,Engine_volume,Mileage,Cylinders,Gear_box_type