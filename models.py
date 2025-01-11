from db import Base, engine
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional

class SensorModel(Base):
    __tablename__='sensors'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    max_results = Column(Integer)
    results = relationship('SensorDataModel', back_populates='sensor', cascade='all, delete')

class SensorDataModel(Base):
    __tablename__='sensor_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(String, ForeignKey('sensors.id'))
    value = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sensor = relationship('SensorModel', back_populates='results')

class Sensor(BaseModel):
    id: int
    name: str
    max_results: int

class ModifySensorDto(BaseModel):
    name: Optional[str] = None
    max_results: Optional[int] = None

class AddSensorData(BaseModel):
    value: float

class SensorData(BaseModel):
    value: float
    timestamp: datetime = datetime.now()

Base.metadata.create_all(bind=engine)