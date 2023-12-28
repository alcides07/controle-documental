from typing import Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status


def get_by_key_value_exists(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    return True if db_object != None else False


def get_by_key_value(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    if (db_object):
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_by_id(db: Session, model: Any, id: int):
    db_object = db.query(model).filter(model.id == id).first()
    if (db_object):
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_all(db: Session, model: Any):
    db_objects = db.query(model)
    return db_objects.all()


def create_object(db: Session, model: Any, schema: Any):
    db_object = model(**schema.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


def delete_object(db: Session, model: Any, id: int):
    db_object = db.query(model).filter(model.id == id).first()
    if (db_object):
        db.delete(db_object)
        db.commit()
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def update_total(db: Session, model: Any, id: int, data: Any):
    db_object = db.query(model).filter(model.id == id).first()
    if (db_object):
        for key, value in vars(data).items():
            if key != "_sa_instance_state":
                setattr(db_object, key, value)
        db.commit()
        return db_object

    raise HTTPException(status.HTTP_404_NOT_FOUND)
