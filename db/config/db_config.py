from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ip_db = 'localhost'
port_db = '3306'
database = 'pdv'
db_user = 'root'
#db_pass = 'AfcItz2320,.'
db_pass = 'admin'
url_db = f'{db_user}:{db_pass}@{ip_db}:{port_db}/{database}'

engine = create_engine(f'mysql+pymysql://{url_db}', pool_size=10, max_overflow=30,
                       pool_timeout=30, pool_recycle=1800)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()