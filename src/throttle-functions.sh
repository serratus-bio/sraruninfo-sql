aws lambda put-function-concurrency \
    --function-name srarun-upload-manager \
    --reserved-concurrent-executions 0

aws lambda put-function-concurrency \
    --function-name srarun-upload-worker \
    --reserved-concurrent-executions 0
