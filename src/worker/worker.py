import pandas as pd
from aurora import upload
from data_config import col_name_map, col_dtype_map
from download import get_contents


def handler(event, context):
    process(event['start_byte'], event['end_byte'])


def process(start_byte, end_byte):
    """read [start_byte, end_byte)"""
    contents = get_contents(start_byte, end_byte - 1)

    df = pd.read_csv(contents,
        header=None,
        names=col_name_map.values(),
        dtype=col_dtype_map)
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d %H:%M:%S')
    df['load_date'] = pd.to_datetime(df['load_date'], format='%Y-%m-%d %H:%M:%S')
    upload(df)
    return df
