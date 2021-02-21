pushd manager
zip -rq package .
aws lambda create-function \
    --function-name srarun-upload-manager \
    --runtime python3.8 \
    --handler manager.handler \
    --timeout 70 \
    --memory-size 10240 \
    --zip-file fileb://./package.zip \
    --role arn:aws:iam::797308887321:role/service-role/biosample-upload-manager-role
rm package.zip
popd

pushd worker
zip -rq package .
aws lambda create-function \
    --function-name srarun-upload-worker \
    --runtime python3.7 \
    --handler worker.handler \
    --timeout 900 \
    --memory-size 10240 \
    --zip-file fileb://./package.zip \
    --role arn:aws:iam::797308887321:role/service-role/biosample-upload-worker-role \
    --layers "arn:aws:lambda:us-east-1:797308887321:layer:biosample-upload:8"
rm package.zip
popd

aws lambda update-function-event-invoke-config \
    --function-name srarun-upload-manager \
    --maximum-retry-attempts 0 \
    --maximum-event-age-in-seconds 60

aws lambda update-function-event-invoke-config \
    --function-name srarun-upload-worker \
    --maximum-retry-attempts 0 \
    --maximum-event-age-in-seconds 60
