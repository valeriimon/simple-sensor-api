from fastapi import FastAPI, HTTPException
from typing import List
from models import Sensor, SensorData, SensorModel, SensorDataModel, ModifySensorDto, AddSensorData
from deps import SessionDep
from sqlalchemy.orm import Session

app = FastAPI()

@app.get('/api/sensors', response_model=List[Sensor])
def get_sensors(db: SessionDep):
    return db.query(SensorModel).all()


@app.post('/api/sensors/', status_code=201, response_model=Sensor)
def create_sensor(sensor: ModifySensorDto, db: SessionDep):
    new_sensor = SensorModel(name=sensor.name, max_results=sensor.max_results)
    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)
    return new_sensor


@app.put('/api/sensors/{sensor_id}', response_model=Sensor)
def update_sensor(sensor_id: str, sensor: ModifySensorDto, db: SessionDep):
    db_sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not db_sensor:
        db.close()
        raise HTTPException(status_code=404, detail='Sensor not found.')
    db_sensor.max_results = sensor.max_results or db_sensor.max_results
    db_sensor.name = sensor.name or db_sensor.name
    db.commit()
    db.refresh(db_sensor)

    # Clean up old data if necessary
    delete_extra_sensor_data(db, db_sensor)

    return db_sensor


@app.delete('/api/sensors/{sensor_id}')
def delete_sensor(sensor_id: str, db: SessionDep):
    db_sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not db_sensor:
        db.close()
        raise HTTPException(status_code=404, detail='Sensor not found.')
    db.delete(db_sensor)
    db.commit()
    return {"message": "Sensor deleted successfully."}


@app.get('/api/sensors/{sensor_id}/data', response_model=List[SensorData])
def get_sensor_data(sensor_id: str, db: SessionDep):
    db_sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail='Sensor not found.')

    data = db.query(SensorDataModel).filter(SensorDataModel.sensor_id == sensor_id).order_by(
        SensorDataModel.timestamp.desc()).all()

    return [SensorData(value=record.value, timestamp=record.timestamp) for record in data]


@app.post('/api/sensors/{sensor_id}/data')
def add_sensor_data(sensor_id: str, data: AddSensorData, db: SessionDep):
    db_sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail='Sensor not found.')

    # Append new data
    new_data = SensorDataModel(sensor_id=sensor_id, value=data.value)
    db.add(new_data)
    db.commit()

    # Clean up old data if necessary
    db.refresh(db_sensor)
    delete_extra_sensor_data(db, db_sensor)

    return {"message": "Sensor data added successfully."}

def delete_extra_sensor_data(db: Session, sensor: SensorModel):
    if len(sensor.results) > sensor.max_results:
        delete_count = len(sensor.results) - sensor.max_results
        to_delete = db.query(SensorDataModel).filter(SensorDataModel.sensor_id == sensor.id).order_by(
            SensorDataModel.timestamp.asc()).limit(delete_count).all()
        for record in to_delete:
            db.delete(record)
        db.commit()


