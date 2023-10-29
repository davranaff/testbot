from dotenv import get_key

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base

_path_to_env = ".env"

_db_user = get_key(_path_to_env, "DB_USER")
_db_host = get_key(_path_to_env, "DB_HOST")
_db_port = get_key(_path_to_env, "DB_PORT")
_db_name = get_key(_path_to_env, "DB_NAME")

engine = create_engine(f'postgresql://{_db_user}@{_db_host}:{_db_port}/{_db_name}')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()