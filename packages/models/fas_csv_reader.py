import csv
from typing import Callable, Optional

FAS_FIELDS_NAMES = [
    'id',
    'link',
    'header',
    'kind',
    'publish_date',
    'department',
    'scope',
    'doc_number',
    'case_number',
    'attach_links',
    'text'
]


def read_csv_to_callback(file_name: str,
                         callback: Optional[Callable]=None,
                         callback_batch_size: Optional[int]=None,
                         max_rows: Optional[int]=None
                         ) -> None:
    with open(file_name) as f:
        current_row = 0
        header_readied = False
        batch = []
        reader = csv.DictReader(f, fieldnames=FAS_FIELDS_NAMES)
        for row in reader:
            if not max_rows or (max_rows and current_row <= max_rows):
                if not header_readied:
                    header_readied = True
                    continue
                elif not callback_batch_size:
                    callback(row)
                elif callback_batch_size:
                    batch.append(row)
                    if len(batch) == callback_batch_size:
                        callback(batch)
                        batch = []
                current_row += 1
            else:
                if callback_batch_size and len(batch):
                    callback(batch)
                break
