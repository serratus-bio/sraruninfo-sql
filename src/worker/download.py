import boto3
s3 = boto3.resource('s3')
s3_object = s3.Object(bucket_name='serratus-aurora', key='biosample/global_SraRunInfo.csv')

def get_contents(start_byte, end_byte=None):
    if not end_byte:
        end_byte = ''
    return s3_object.get(Range=f'bytes={start_byte}-{end_byte}')['Body']
