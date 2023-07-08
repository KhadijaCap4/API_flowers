from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://jardindedendb_user:JrFSfPObNaBpXw0TTln7DZILqmGH8MGr@dpg-ciimtjdgkuvojjbv1s40-a.frankfurt-postgres.render.com/jardindedendb'

# Create the database engine
database_engine = create_engine(DATABASE_URL)

# Create a session template for interacting with the database
SessionTemplate = sessionmaker(
    bind=database_engine, autocommit=False, autoflush=False)

# get_cursor is used by almost all endpoint in order to connect to the database
def get_cursor():
    # Create a new session
    db = SessionTemplate()
    try:
        yield db # Use yield to return the session as a context manager
    finally:
        db.close() # Close the session after it is used
