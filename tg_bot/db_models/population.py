from .base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)


class Population(BaseModel):
    __tablename__ = 'population'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime())
    population = Column(Integer)
