
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    '''Table for keeping information about users'''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    votes = relationship("Vote", back_populates="owner")
    quizzes = relationship("Quiz", back_populates="owner")
    answers = relationship("VoteUserAnswer", back_populates="user_answer")


class Vote(Base):
    '''Table for keeping title and question of votes'''
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    question = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    vote_answers = relationship("VoteAnswer", back_populates="vote")
    owner = relationship("User", back_populates="votes")
    user_answers = relationship("VoteUserAnswer", back_populates="vote")


class VoteAnswer(Base):
    '''Table for keeping vote answers'''
    __tablename__ = "vote_answers"
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, index=True)
    vote_id = Column(Integer, ForeignKey("votes.id"))
    is_it_true = Column(Boolean, default=False)
    vote = relationship("Vote", back_populates="vote_answers")


class VoteUserAnswers(Base):
    '''Table for keeping answers of users'''
    __tablename__ = "vote_user_answers"
    id = Column(Integer, primary_key=True, index=True)    
    answer_id = Column(Integer, ForeignKey("vote_answers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    user_answer = relationship("User", back_populates="answers")
    vote = relationship("Vote", back_populates="user_answers")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    is_required_input = Column(Boolean, default=False)
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question")
    custom_answers = relationship("QuizCustomAnswer", back_populates="question")


class QuizAnswer(Base):
    __tablename__ = "quiz_anwers"
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    is_it_true = Column(Boolean, default=False)
    question = relationship("QuizQuestion", back_populates="answers")
    

class QuizCustomAnswer(Base):
    __tablename__ = "custom_answer"
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    question = relationship("QuizQuestion", back_populates="custom_answers")
