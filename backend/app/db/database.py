from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# metadata = MetaData(
#     naming_convention={
#         'ix': 'ix_%(column_0_label)s',
#         'uq': 'uq_%(table_name)s_%(column_0_name)s',
#         'ck': 'ck_%(table_name)s_%(constraint_name)s',
#         'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
#         'pk': 'pk_%(table_name)s'
#     }
# )
#
# Base = declarative_base(metadata=metadata)
Base = declarative_base()
