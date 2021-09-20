
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class QuizCustomAnswerBase(BaseModel):
    answer = str


class QuizCustomAnswer(QuizCustomAnswerBase):
    pass


class QuizCustomAnswer(QuizCustomAnswerBase):
    id: int
    question_id: int
    author_id: int
    class Config:
        orm_mode = True


class QuizAnswerBase(BaseModel):
    answer: str


class QuizAnswerCreate(QuizAnswerBase):
    pass


class QuizAnswer(QuizAnswerBase):
    id: int
    question_id: int
    class Config:
        orm_mode = True


class QuizQuestionBase(BaseModel):
    question: str


class QuizQuestionCreate(QuizQuestionBase):
    pass


class QuizQuestion(QuizQuestionBase):
    id: int
    quiz_id: int
    answers: List[QuizAnswer] = []
    custom_answers: List[QuizCustomAnswer] = []
    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    title: str


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase):
    id: int
    owner_id: int
    questions: List[QuizQuestion] = []
    class Config:
        orm_mode = True


class VoteUserAnswerBase(BaseModel):
    answer_id: int
    user_id: int


class VoteUserAnswerCreate(VoteUserAnswerBase):
    pass


class VoteUserAnswer(VoteUserAnswerBase):
    id: int


class VoteAnswerBase(BaseModel):
    answer: str
    is_it_true: bool


class VoteAnswerCreate(VoteAnswerBase):
    pass


class VoteAnswer(VoteAnswerBase):
    id: int
    vote_id: int
    class Config:
        orm_mode = True


class VoteBase(BaseModel):
    title: str
    question: Optional[str] = None


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int
    owner_id: int
    vote_answers: List[VoteAnswer] = []
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    votes: List[Vote] = []
    quizzes: List[Quiz] = []
    class Config:
        orm_mode = True   
