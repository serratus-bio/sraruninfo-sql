from lambda_helpers import invoke_lambda
import boto3

s3 = boto3.resource('s3')
s3_object = s3.Object(bucket_name='serratus-aurora', key='biosample/global_SraRunInfo.csv')

WORKER_LAMBDA = 'srarun-upload-worker'
MAX_ITEMS_PER_WORKER = 1000
MINIMUN_REMAINING_TIME_MS = 10000

def handler(event, context):
    start_byte = event.get('start_byte', 0)
    end = s3_object.content_length
    print(f'start: {start_byte} total: {end}')
    while start_byte < end:
        if context and context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
            print(f'10s left. stopping this manager.')
            break
        start_byte = prepare_worker(start_byte)
    if start_byte < end:
        print(f'invoking new manager: {start_byte}')
        invoke_new_manager(context, start_byte)
    else:
        print(f'invoking final worker: {start_byte}')
        invoke_worker(start_byte, end)


def get_contents(start_byte, end_byte=None):
    if not end_byte:
        end_byte = ''
    return s3_object.get(Range=f'bytes={start_byte}-{end_byte}')['Body']


def prepare_worker(start_byte):
    f = get_contents(start_byte)
    lines = f.iter_lines()
    if start_byte == 0:
        start_byte += len(next(lines)) + 1 # skip csv header

    count = 0
    n_bytes = 0
    for line in lines:
        n_bytes += len(line) + 1
        count += 1
        if count == MAX_ITEMS_PER_WORKER:
            break

    end_byte = start_byte + n_bytes
    print(f'invoking worker with start={start_byte},end={end_byte}')
    invoke_worker(start_byte, end_byte)
    return end_byte


def invoke_worker(start_byte, end_byte):
    event = {'start_byte': start_byte, 'end_byte': end_byte}
    invoke_lambda(WORKER_LAMBDA, event)


def invoke_new_manager(context, next_start_byte):
    # invoke next manager instance
    next_event = {
        'start_byte': next_start_byte
    }
    invoke_lambda(context.function_name, next_event)
