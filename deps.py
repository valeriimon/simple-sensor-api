from db import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

# Dependency to get the database session
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

SessionDep = Annotated[Session, Depends(get_db)]