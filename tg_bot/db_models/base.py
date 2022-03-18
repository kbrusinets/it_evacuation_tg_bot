from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from os import environ

__all__ = (
    'BaseModel',
)

metadata = MetaData(schema=environ.get("SCHEMA_NAME"))
BaseModel = declarative_base(metadata=metadata)
