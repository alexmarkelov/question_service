
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=schemas.User)
def get_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found") 
    return db_user


@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.UserCreate, email: str,
                db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    new_email_user = crud.get_user_by_email(db, user.email)
    if new_email_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    return crud.update_user(db, user, email)


@app.delete("/users/", response_model=schemas.User) 
def remove_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    return crud.remove_user(db, email)


@app.post("/votes/", response_model=schemas.Vote)
def create_vote(vote: schemas.VoteCreate, user_id: int,\
                db: Session = Depends(get_db)):
    return crud.create_vote(db, vote, user_id)


@app.get("/votes/", response_model=schemas.Vote)
def get_vote(vote_id, db: Session = Depends(get_db)):
    db_vote = crud.get_vote(db, vote_id)
    if not db_vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return db_vote


@app.put("/votes/", response_model=schemas.Vote)
def update_vote(vote: schemas.VoteCreate, vote_id: int,\
                db: Session = Depends(get_db)):
    db_vote = crud.get_vote(db, vote_id)
    if not db_vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return crud.update_vote(db, vote, vote_id)


@app.delete("/votes/", response_model=schemas.Vote)
def remove_vote(vote_id: int, db: Session = Depends(get_db)):
    db_vote = crud.get_vote(db, vote_id)
    if not db_vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return crud.remove_vote(db, vote_id)


@app.post("/votes/answers/", response_model=schemas.VoteAnswer)
def create_vote_answer(answer: schemas.VoteAnswerCreate, vote_id: int,\
                       db: Session = Depends(get_db)):
    return crud.create_vote_answer(db, answer, vote_id)


@app.get("/votes/answers/", response_model=schemas.VoteAnswer)
def get_vote_answer(answer_id: int, db: Session = Depends(get_db)):
    return crud.get_vote_answer(db, answer_id)


@app.put("/votes/answers/", response_model=schemas.VoteAnswer)
def update_vote_answer(answer: schemas.VoteAnswerCreate, answer_id: int,\
                       db: Session = Depends(get_db)):
    db_answer = crud.get_vote_answer(db, answer_id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="VoteAnwser not found")
    return crud.update_vote_answer(db, answer, answer_id)


@app.delete("/votes/answers/", response_model=schemas.VoteAnswer)
def remove_vote_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud.get_vote_answer(db, answer_id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="VoteAnswer not found")
    return crud.remove_vote_answer(db, answer_id)


@app.post("/votes/useranswer/", response_model=schemas.VoteAnswer)
def add_new_user_answer(answer: schemas.VoteUserAnswerCreate,\
                        db: Session = Depends(get_db)):
    user_answer = user_create_answer(db, answer)
    return user_answer
