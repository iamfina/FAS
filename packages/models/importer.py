import csv
from functools import partial
from typing import Callable, Optional, List
from pony import orm
from models import RawFas, FAS_FIELDS_NAMES

__slots__ = []


CLASSES_MAPS = {
    'fas': (RawFas, FAS_FIELDS_NAMES)
}


def read_csv_to_callback(file_name: str,
                         fields_list: List[str],
                         callback: Optional[Callable]=None,
                         callback_batch_size: Optional[int]=None,
                         max_rows: Optional[int]=None
                         ) -> None:
    with open(file_name) as f:
        current_row = 0
        header_readied = False
        batch = []
        reader = csv.DictReader(f, fieldnames=fields_list)
        for row in reader:
            if not max_rows or (max_rows and current_row <= max_rows):
                row.pop('id')
                if not header_readied:
                    header_readied = True
                    continue
                elif not callback_batch_size:
                    callback(**row)
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


@orm.db_session
def create_from_list_rows(rows, cls):
    for r in rows:
        cls(**r)


def create_from_csv(file_name, class_name, batch_size, max_rows):
    cls, fields = CLASSES_MAPS[class_name]
    read_csv_to_callback(
        file_name=file_name,
        fields_list=fields,
        callback=partial(create_from_list_rows, cls=cls),
        callback_batch_size=batch_size,
        max_rows=max_rows
    )


if __name__ == '__main__':
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description='Process csv file to db.')
    parser.add_argument('--file_name',
                        type=str,
                        required=True,
                        help='file for read')
    parser.add_argument('--class_name',
                        type=str,
                        choices=['fas', 'zakupki'],
                        required=True,
                        help='class for save in db')
    parser.add_argument('--batch_size',
                        type=int,
                        default=1000,
                        help='number of rows insert per db transaction')
    parser.add_argument('--max_rows',
                        type=int,
                        default=0,
                        help='Max number of rows readied and inserted')

    args = parser.parse_args()
    print(f' ---\n File name: {args.file_name}')
    print(f' Class name: {args.class_name}')
    print(f' Batch size: {args.batch_size}')
    print(f' Max rows: {args.max_rows}')
    print(f' ---\n Start at: {datetime.utcnow()}')
    create_from_csv(
        file_name=args.file_name,
        class_name=args.class_name,
        batch_size=args.batch_size,
        max_rows=args.max_rows
    )
    print(f' Stop at: {datetime.utcnow()}')
