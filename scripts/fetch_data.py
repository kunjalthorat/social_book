import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Create the database engine
engine = create_engine('postgresql://postgres:root@localhost:5432/social_book')

# Fetch data from the upload_book table
df = pd.read_sql('SELECT * FROM upload_book', engine)
print(df)

# Fetch data from the accounts_customuser table
df1 = pd.read_sql('SELECT * FROM accounts_customuser', engine)
print(df1)

# Fetch data from the upload_book table ordered by id
df2 = pd.read_sql('SELECT * FROM public.upload_book ORDER BY id ASC', engine)
print(df2)
