from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from.. import models,schemas,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/",response_model=List[schemas.PostOut]) #Without response_model, FastAPI works but loses data validation, auto-docs, and type safety - your endpoint returns data but FastAPI won't validate or properly document the response structure.
def test_posts(db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user),
               limit:int = 10, skip : int =0, search: Optional[str] = ""):  #Rate Limiter(For pagination.)
    
    #get_post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    get_post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True). group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return get_post

@router.get("/{id}",response_model=schemas.PostOut)  #Get post by id
def get_post(id:int, db:Session = Depends(get_db), user_id :int = Depends(oauth2.get_current_user)):

   # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True). group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} was not found.")

    return  post

#CREATE POST
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #CREATE POST
def create_post(post : schemas.PostCreate, 
                db:Session = Depends(get_db),
                current_user: schemas.Token_Data = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#DELETE POST BY ID
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int,  db:Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
   

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = delete_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")\
                            
    #Check whether the user logged in has access to only his post.
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail= f'Unauthorized access.')
    
    delete_post_query.delete()
    db.commit()

#UPDATE POST BY ID
@router.put("/{id}", response_model=schemas.Post)  #update post by id
def update_post(id : int, post : schemas.PostCreate, db:Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):  #FastAPI converts it into a Posts object. post is a pydantic object.


    updated_post_query =db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()  #.first() executes the query and returns a Post object.

    #Check whether the user logged in has access to only hs post. 
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found.")
    
    #updated_post.owner_id → ID of the user who created the post.
    #current_user.id → ID of the currently logged-in user (from the JWT token).
    if updated_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail= f'Unauthorized access.')
    
    updated_post_query.update(post.dict())  #Query.update() performs an SQL UPDATE.
    db.commit()
  
    return  updated_post