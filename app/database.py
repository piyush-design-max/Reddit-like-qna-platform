from fastapi import Depends
from sqlmodel import Session, create_engine
from .config import settings
from typing import Annotated

DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'



engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session

getdb_dependency = Annotated[Session, Depends(get_db)]