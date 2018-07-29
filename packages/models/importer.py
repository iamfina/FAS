#! /usr/bin/python

import os
import sys
import csv
import logging
from functools import partial
from typing import Callable, Optional, List
from pony import orm
from models import RawFas, Raw222Fz, Raw44Fz, FAS_FIELDS_NAMES, FZ233_FIELDS_NAMES, FZ44_FIELDS_NAMES

csv.field_size_limit(sys.maxsize)
logger = logging.getLogger('DataImporter')
FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.NOTSET)

CLASSES_MAPS = {
    'fas': (RawFas, FAS_FIELDS_NAMES),
    '223fz': (Raw222Fz, FZ233_FIELDS_NAMES),
    '44fz': (Raw44Fz, FZ44_FIELDS_NAMES)
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
                if 'id' in row:
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


def create_from_csv(path: str, class_name: str, batch_size: int, max_rows: int):
    cls, fields = CLASSES_MAPS[class_name]
    if os.path.isfile(path):
        read_csv_to_callback(
            file_name=path,
            fields_list=fields,
            callback=partial(create_from_list_rows, cls=cls),
            callback_batch_size=batch_size,
            max_rows=max_rows
        )
    else:
        files = filter(lambda x: x.endswith('.csv'), os.listdir(path))
        logging.info(f'Path {path} is dir')
        for f in files:
            try:
                logging.info(f'Start import {f} from {path}')
                cls_with_filename = partial(cls, source_filename=f)
                read_csv_to_callback(
                    file_name=f,
                    fields_list=fields,
                    callback=partial(create_from_list_rows, cls=cls_with_filename),
                    callback_batch_size=batch_size,
                    max_rows=max_rows
                )
            except Exception as e:
                logger.error(e)
            finally:
                logging.info(f'Stop import {f} from {path}')



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process csv file or path with csv files to db.')
    parser.add_argument('--path',
                        type=str,
                        required=True,
                        help='Directory or file for read')
    parser.add_argument('--class_name',
                        type=str,
                        choices=['fas', '223fz', '44fz'],
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
    logger.info(f'Path name: {args.path}')
    logger.info(f'Class name: {args.class_name}')
    logger.info(f'Batch size: {args.batch_size}')
    logger.info(f'Max rows: {args.max_rows}')
    logger.info('Start import')
    create_from_csv(
        path=args.path,
        class_name=args.class_name,
        batch_size=args.batch_size,
        max_rows=args.max_rows
    )
    logger.info('Stop import')
