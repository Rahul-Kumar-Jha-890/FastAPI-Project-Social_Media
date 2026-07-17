from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from .. import schemas,database,oauth2,models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(database.get_db),
         current_user : int = Depends(oauth2.get_current_user)):    

#First check whether the post exists in our Post db or not
        post =  db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
        if not post:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#models.Vote.post_id → the post_id column in the database. vote.post_id → the post_id received in the request body.
#The use case of this query is to determine whether the current user has already voted for a specific post.

        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                        models.Vote.user_id == current_user.id)
         
        found_vote = vote_query.first()

        if(vote.dir==1):  #User wants to add a vote.
            if found_vote:
                  raise HTTPException(status.HTTP_409_CONFLICT,
                 detail=f'User {current_user.id} has already voted for post with id of  {vote.post_id}')

#models.Vote creates a new vote object with the post ID and the current user's ID, ready to be saved to the database.
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return({"Message" : "Vote added successfully"})
         
        else:
               if not found_vote:
                     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exist.')
                
               vote_query.delete(synchronize_session=False)
               db.commit()
               return({"Message" : "Vote deleted successfully."})