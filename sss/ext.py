from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import types
import sqlalchemy.dialects.postgresql as pg
import uuid


db = SQLAlchemy()


class UUID(types.TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = types.CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(pg.UUID() if dialect.name == 'postgresql' else types.CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            return "%.32x" % (uuid.UUID(value) if not isinstance(value, uuid.UUID) else value)

    def process_result_value(self, value, dialect):
        return value if value is None else uuid.UUID(value)


# Credit goes to http://www.luckydonkey.com/2008/07/27/sqlalchemy-migrate-upgrade-scripts-in-a-transaction/
def transaction(f, *args, **kwargs):
    def wrapper(migrate_engine, *args, **kwargs):
        connection = migrate_engine.connect()
        transaction = connection.begin()
        try:
            result = f(migrate_engine, *args, **kwargs)
            transaction.commit()
            return result
        except:
            transaction.rollback()
            raise
        finally:
            connection.close()

    wrapper.__name__ = f.__name__
    wrapper.__dict__ = f.__dict__
    wrapper.__doc__ = f.__doc__
    return wrapper

# Inject UUID type to SQLAlchemy
db.UUID = UUID()
