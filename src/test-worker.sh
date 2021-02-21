aws lambda invoke \
    --function-name srarun-upload-worker \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "start_byte": 520, "end_byte": 467853 }' \
    response.json
