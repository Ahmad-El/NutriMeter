from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

## loading environment variables
load_dotenv()
ENV = os.getenv

## connecting to postgresql and creating session
db_url = f"postgresql://{ENV('user')}:{ENV('password')}@{ENV('host')}:{ENV('port')}/{ENV('dbname')}"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
