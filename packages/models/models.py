from os import environ as _e
from pony import orm

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


FZ233_FIELDS_NAMES = [
    'reg_num',
    'type',
    'created_at',
    'url',
    'ETP_url',
    'fullname',
    'customer',
    'customer_INN',
    'ETP',
    'docs_start',
    'docs_end',
    'not_dishonest',
    'attach_count',
    'attach_urls',
    'modified_at',
    'same_place',
    'emergency',
    'examination_at',
    'summing_at',
    'submission_deadline',
    'total_max_sum',
    'OKPD',
    'OKVED',
    'small_contarctor',
    'excluded_from_plan',
    'small_subcontractor',
    'ignored',
    'centralized',
    'deliveryplace',
    'extend_fields',
    'lots_descriptions'
]


class Raw222Fz(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    reg_num = orm.Optional(str)
    type = orm.Optional(str)
    created_at = orm.Optional(str)
    url = orm.Optional(str)
    ETP_url = orm.Optional(str)
    fullname = orm.Optional(str)
    customer = orm.Optional(str)
    customer_INN = orm.Optional(str)
    ETP = orm.Optional(str)
    docs_start = orm.Optional(str)
    docs_end = orm.Optional(str)
    not_dishonest = orm.Optional(str)
    attach_count = orm.Optional(str)
    attach_urls = orm.Optional(str)
    modified_at = orm.Optional(str)
    same_place = orm.Optional(str)
    emergency = orm.Optional(str)
    examination_at = orm.Optional(str)
    summing_at = orm.Optional(str)
    submission_deadline = orm.Optional(str)
    total_max_sum = orm.Optional(str)
    OKPD = orm.Optional(str)
    OKVED = orm.Optional(str)
    small_contarctor = orm.Optional(str)
    excluded_from_plan = orm.Optional(str)
    small_subcontractor = orm.Optional(str)
    ignored = orm.Optional(str)
    centralized = orm.Optional(str)
    deliveryplace = orm.Optional(str)
    extend_fields = orm.Optional(str)
    lots_descriptions = orm.Optional(str)


db.generate_mapping(create_tables=True)
