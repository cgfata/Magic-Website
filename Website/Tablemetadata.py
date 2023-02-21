import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

BOT_TOKEN = os.environ.get('TOKEN')
MAGIC_INVENTORY_HOST = os.environ.get('HOST')
MAGIC_INVENTORY_USER = os.environ.get('USER')
MAGIC_INVENTORY_PASSWORD = os.environ.get('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.environ.get('DATABASE')
MAGIC_INVENTORY_PASSWORD_AZURE = os.environ.get('PASSWORD_AZURE')
MAGIC_INVENTORY_HOST_AZURE = os.environ.get('HOST_AZURE')


engine = create_engine(f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD_AZURE}@{MAGIC_INVENTORY_HOST_AZURE}:3306/{MAGIC_INVENTORY_DATABASE}')
metadata = MetaData(bind=engine)

# reflect the tables in the database
metadata.reflect()

# create session factory
Session = sessionmaker(bind=engine)

# create model classes for each reflected table
for table in metadata.tables.values():
    name = table.name.capitalize()
    cls = type(name, (object,), {})
    mapper(cls, table)
    globals()[name] = cls