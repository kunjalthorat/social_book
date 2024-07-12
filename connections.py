from sqlalchemy import create_engine

# Replace these placeholders with your actual database credentials
db_username = 'postgres'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'social_book'

# Create the database URL
db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Check if the engine is working by trying to connect
try:
    engine.connect()
    print('Connection successful!')
except Exception as e:
    print('Error connecting to the database:', e)
