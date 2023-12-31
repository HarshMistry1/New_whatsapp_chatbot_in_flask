from multi_tenant.models import Tenant
from multi_tenant.models import db
from multi_tenant.new_one import simple_cache
from flask import current_app

MYSQL_URI = 'mysql+pymysql://user:pwd@localhost/{}?charset=utf8'


@simple_cache
def get_known_tenants():
    tenants = Tenant.query.all()
    return [i.name for i in tenants]


def prepare_bind(tenant_name):
    if tenant_name not in current_app.config['SQLALCHEMY_BINDS']:
        current_app.config['SQLALCHEMY_BINDS'][tenant_name] = MYSQL_URI.format(tenant_name)
    return current_app.config['SQLALCHEMY_BINDS'][tenant_name]


def get_tenant_session(tenant_name):
    if tenant_name not in get_known_tenants():
        return None
    prepare_bind(tenant_name)
    engine = db.get_engine(current_app, bind=tenant_name)
    session_maker = db.sessionmaker()
    session_maker.configure(bind=engine)
    session = session_maker()
    return session