from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from.. import models,schemas,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])



@router.get("/",response_model=List[schemas.Post]) #Without response_model, FastAPI works but loses data validation, auto-docs, and type safety - your endpoint returns data but FastAPI won't validate or properly document the response structure.
def test_posts(db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user)):
    get_post = db.query(models.Post).all()
    return get_post

@router.get("/{id}",response_model=schemas.Post)  #Get post by id
def get_post(id:int, db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} was not found.")

    return  post

#CREATE POST
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #CREATE POST
def create_post(post : schemas.PostCreate, db:Session = Depends(get_db),user_id :int = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#DELETE POST BY ID
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int,  db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user)):
   

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    
    deleted_post.delete()
    db.commit()

#UPDATE POST BY ID
@router.put("/{id}", response_model=schemas.Post)  #update post by id
def update_post(id : int, post : schemas.PostCreate, db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user)):  #FastAPI converts it into a Posts object. post is a pydantic object.


    updated_post=db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    
    updated_post.update(post.dict())
    db.commit()
  
    return  updated_post.first()
