from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models.user import User
from orm.common.index import delete_object, get_by_key_value_exists, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.user import UserCreate, UserRead
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/",
            response_model=List[UserRead],
            summary="Lista usuários",
            dependencies=[Depends(get_authenticated_user)],
            )
def read(
        db: Session = Depends(get_db),
):
    users = get_all(db, User)

    return users


@router.get("/{id}/",
            response_model=UserRead,
            summary="Lista um usuário",
            dependencies=[Depends(get_authenticated_user)],

            )
def read_id(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)
):
    users = jsonable_encoder(get_by_id(db, User, id))

    return users


@router.post("/",
             response_model=UserRead,
             status_code=201,
             summary="Cadastra um usuário",
             )
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    if (user.password != user.passwordConfirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. As senhas fornecidas não coincidem!")

    elif (get_by_key_value_exists(db, User, "username", user.username)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O nome de usuário fornecido está em uso!")

    elif (get_by_key_value_exists(db, User, "email", user.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O e-mail fornecido está em uso!")

    else:
        user.password = pwd_context.hash(user.password)
        data = jsonable_encoder(create_user(db=db, user=user))

        return data


@router.delete("/{id}/",
               response_model=UserRead,
               summary="Deleta um usuário",
               dependencies=[Depends(get_authenticated_user)],
               )
def delete(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)
):

    user = jsonable_encoder(delete_object(db, User, id))
    return user
