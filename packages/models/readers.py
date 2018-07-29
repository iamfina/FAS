import sys
import os
import json as _json
import pandas as _pandas


def _read_table_to_pandas(table_name, offset: int=0, limit: int=10000) -> '_pandas.DataFrame':
    assert isinstance(offset, int)
    assert isinstance(limit, int)
    with open(os.path.join(sys.prefix, 'credentials.json')) as f:
        credentials = _json.load(f)
    connection_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**credentials)
    return _pandas.read_sql(
        f'SELECT * FROM {table_name} ORDER BY id ASC OFFSET {offset} LIMIT {limit}',
        connection_string
    )


def read_rawfas_to_pandas(offset: int=0, limit: int=10000) -> '_pandas.DataFrame':
    return _read_table_to_pandas('rawfas', offset, limit)


def read_223fz_to_pandas(offset: int=0, limit: int=10000) -> '_pandas.DataFrame':
    return _read_table_to_pandas('raw222fz', offset, limit)


def read_44fz_to_pandas(offset: int=0, limit: int=10000) -> '_pandas.DataFrame':
    return _read_table_to_pandas('raw44fz', offset, limit)
