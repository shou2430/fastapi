from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..schemas import VoteInfo
from .. import models, oauth2

router = APIRouter(
    prefix="/votes",
    tags=["votes"] # this will be used to group the routes in the documentation
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteInfo, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    print('find post')
    # check if the user has already voted for the post
    vote_exists = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).first()
    print(vote_exists)
    # if the vote exists and the user still want to vote, raise an exception
    if vote_exists and vote.switch == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you have already voted for this post")
    
    # if the vote deosn't exist and the user want to unvote, raise an exception
    if not vote_exists and vote.switch == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you have not voted for this post")
    
    # if the vote exists and the user want to unvote, delete the vote
    if vote_exists:
        db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).delete()
        db.commit()
        return {"message": "vote deleted successfully"}
    
    # if the vote doesn't exist and the user want to vote, create the vote
    new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
    db.add(new_vote)
    db.commit()    
    return {"message": "vote created successfully"}
