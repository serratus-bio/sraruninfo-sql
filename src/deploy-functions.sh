pushd manager
zip -rq package .
aws lambda update-function-code \
    --function-name srarun-upload-manager \
    --zip-file fileb://./package.zip
rm package.zip
popd

pushd worker
zip -rq package .
aws lambda update-function-code \
    --function-name srarun-upload-worker \
    --zip-file fileb://./package.zip
rm package.zip
popd
