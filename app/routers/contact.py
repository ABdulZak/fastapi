from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix='/contacts', tags=['Contact'])

@router.get('/', response_model=List[schemas.ContactOut])
async def get_contacts(db: Session= Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    results = db.query(models.Contact, func.count(models.Vote.contact_id).label('votes')).join(models.Vote, models.Vote.contact_id == models.Contact.id, isouter=True).group_by(models.Contact.id).all()
    return results


@router.get('/{id}', response_model=schemas.ContactOut)
async def get_contact(id:int,db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    contact = db.query(models.Contact, func.count(models.Vote.contact_id).label('votes')).join(models.Vote, models.Vote.contact_id == models.Contact.id, isouter=True).group_by(models.Contact.id).filter(models.Contact.id == id).first()
    if contact == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id:{id}")
    return contact

@router.post('/', response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(contact:schemas.CreateContact, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    created_contact = models.Contact(owner_id = current_user.id,**contact.dict())
    db.add(created_contact)
    db.commit()
    db.refresh(created_contact)
    return created_contact

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Contact).filter(models.Contact.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.ContactOut)
def change_contact(id:int, contact:schemas.CreateContact, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_query = db.query(models.Contact).filter(models.Contact.id == id)
    updated_contact = updated_query.first()
    if updated_contact == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {id} was not found")
    if updated_contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed action")
    updated_query.update(contact, synchronize_session=False)
    db.commit()
    return updated_query.first() 