from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

# Database connection URL
DATABASE_URL = 'postgresql://postgres:root@localhost:5432/social_book'

# Create the database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# MetaData object to hold the schema of the database
metadata = MetaData()

def fetch_data_from_table(table_name):
    # Reflect the table from the database
    table = Table(table_name, metadata, autoload_with=engine)
    stmt = select([table])
    with engine.connect() as connection:
        result = connection.execute(stmt)
        for row in result:
            print(row)
