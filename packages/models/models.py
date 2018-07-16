from os import environ as _e
from pony import orm

__slots__ = ['FAS_FIELDS_NAMES', 'RawFas']

db = orm.Database()

db.bind(
    provider='postgres',
    user=_e.get('POSTGRES_USER'),
    password=_e.get('POSTGRES_PASSWORD'),
    host=_e.get('POSTGRES_HOST'),
    database=_e.get('POSTGRES_DB')
)

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


class RawFas(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    link = orm.Optional(str)
    header = orm.Optional(str)
    kind = orm.Optional(str)
    publish_date = orm.Optional(str)
    department = orm.Optional(str)
    scope = orm.Optional(str)
    doc_number = orm.Optional(str)
    case_number = orm.Optional(str)
    attach_links = orm.Optional(str)
    text = orm.Optional(str)


db.generate_mapping(create_tables=True)
