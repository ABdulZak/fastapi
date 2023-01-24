from fastapi import APIRouter, Depends, Response, HTTPException, status
from .. import schemas, models, database, utils
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {id} was not found")
    return user

@router.post('/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db:Session = Depends(database.get_db)):
    created_user = models.User(**user.dict())
    created_user.password = utils.hash(created_user.password)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session = Depends(database.get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == id)
    if contact.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {id} was not found")
    contact.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.UserOut)
def change_user(id:int, user:schemas.CreateUser, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {id} was not found")
    user_query.update(user, synchronize_session=False)
    db.commit()
    return user_query.first()