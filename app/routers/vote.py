from typing import List
from fastapi import APIRouter, HTTPException, Response, status, Depends, FastAPI
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    contact = db.query(models.Contact).filter(models.Contact.id == vote.contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with idd: {vote.contact_id} doesn't exist")
    vote_query = db.query(models.Vote).filter(models.Vote.contact_id == vote.contact_id, models.Vote.user_id == current_user.id)
    found_contact = vote_query.first()
    if vote.dir==1:
        if found_contact:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted")
        new_vote = models.Vote(user_id = current_user.id, contact_id = vote.contact_id)
        db.add(new_vote)
        db.commit()
        return {"mesage":"successfully added vote"}
    else:
        if not found_contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'successfully deleted vote'}

@router.get('/', response_model=List[schemas.VoteOut])
def get_votes(db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    votes = db.query(models.Vote).all()
    return votes