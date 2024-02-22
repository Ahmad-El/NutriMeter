from sqlalchemy import DateTime, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Sport(Base):
    __tablename__ = "sport"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(100))
    met = Column("met", Float)
    duration_min = Column("duration_min", Float)
    calories_kcal = Column("calories_kcal", Float)
    date = Column("date", DateTime)

    def __init__(self, name, met, duration_min, calories_kcal, date) -> None:
        self.name = name
        self.met = met
        self.duration_min = duration_min
        self.calories_kcal = calories_kcal
        self.date = date
