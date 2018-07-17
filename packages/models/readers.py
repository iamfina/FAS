import sys
import os
import json as _json
import pandas as _pandas


def read_rawfas_to_pandas(offset: int=0, limit: int=10000) -> '_pandas.DataFrame':
    assert isinstance(offset, int)
    assert isinstance(limit, int)
    with open(os.path.join(sys.prefix, 'credentials.json')) as f:
        credentials = _json.load(f)
    connection_string = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**credentials)
    return _pandas.read_sql(
        f'SELECT * FROM rawfas ORDER BY id ASC OFFSET {offset} LIMIT {limit}',
        connection_string
    )
