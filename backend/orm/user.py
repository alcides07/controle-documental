from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        **user.model_dump(exclude=set(["passwordConfirmation"])))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, model: Any, id: int, data: Any):
    db_object = db.query(model).filter(model.id == id).first()

    if (db_object):
        for key, value in data.dict().items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
        return db_object

    raise HTTPException(status.HTTP_404_NOT_FOUND)
