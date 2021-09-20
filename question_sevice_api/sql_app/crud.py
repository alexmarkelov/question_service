
from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext


my_crcxt = CryptContext(schemes=["sha256_crypt"])

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(bd: Session, offset: int = 0, limit: int = 10):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = my_crcxt.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    db_user.email = user.email
    db_user.password = my_crcxt.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    db.delete(db_user)
    db_related_votes = db_user.votes
    for vote in db_related_votes:
        db_answers = vote.vote_answers
        for answer in db_answers:
            db.delete(answer)
        db.delete(vote)
    db.commit()
    return db_user


def create_vote(db: Session, item: schemas.VoteCreate ,user_id: int):
    db_vote = models.Vote(**item.dict(), owner_id=user_id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_vote(db: Session, vote_id: int):
    db_vote = db.query(models.Vote).filter(models.Vote.id == vote_id)\
              .first()
    return db_vote


def update_vote(db: Session, vote: schemas.VoteCreate, vote_id: int):
    db_vote = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    db_vote.title = vote.title
    db_vote.question = vote.question
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_votes(db: Session, user_id: int):
    return db.query(models.User.votes).all()


def remove_vote(db:Session, vote_id: int):
    db_vote = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    db.delete(db_vote)
    db_related_answers = db.query(models.VoteAnswer).\
                         filter(models.VoteAnswer.vote_id == vote_id).all()
    for answer in db_related_answers:
        db.delete(answer)
    db.commit()
    return db_vote


def create_vote_answer(db: Session, item: schemas.VoteAnswerCreate,\
                       vote_id: int):
    db_vote_answer = models.VoteAnswer(**item.dict(), vote_id=vote_id)
    db.add(db_vote_answer)
    db.commit()
    db.refresh(db_vote_answer)
    return db_vote_answer


def get_vote_answer(db: Session, answer_id: int):
    db_vote_answer = db.query(models.VoteAnswer).\
                     filter(models.VoteAnswer.id == answer_id).first()
    return db_vote_answer


def update_vote_answer(db: Session, vote_answer: schemas.VoteAnswerCreate,\
                       answer_id: int):
    db_vote_answer = db.query(models.VoteAnswer).\
                     filter(models.VoteAnswer.id == answer_id).first()
    db_vote_answer.answer = vote_answer.answer
    db_vote_answer.is_it_true = vote_answer.is_it_true
    db.commit()
    db.refresh(db_vote_answer)
    return db_vote_answer


def remove_vote_answer(db: Session, answer_id: int):
    db_vote_answer = db.query(models.VoteAnswer).\
                     filter(models.VoteAnswer.id == answer_id).first()
    db.delete(db_vote_answer)
    db.commit()
    return db_vote_answer


def user_create_answer(db: Session, answer: schemas.VoteUserAnswerCreate):
    db_user_answer = models.VoteAnswer(**answer.dict())
    db.add(db_user_answer)
    db.commit()
    db.refresh(db_user_answer)
    return db_user_answer
