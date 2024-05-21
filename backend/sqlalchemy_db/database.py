from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import make_url

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
POSTGRES_URL = make_url()

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
