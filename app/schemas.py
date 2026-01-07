from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


ApplicantType = Literal["common", "yb", "ob"]


class QuestionOut (BaseModel) :
    id: int
    question: str
    applicant_type: ApplicantType
    field_type: str
    required: bool
    max_len: Optional[int] = None
    position: int


class QuestionsResponse (BaseModel) :
    applicant_type: ApplicantType
    questions: List[QuestionOut]


class ApplicationCreate (BaseModel) :
    applicant_type: ApplicantType
    answers: Dict[str, str] = Field(default_factory=dict)


class ApplicationCreated (BaseModel) :
    application_id: int
    status: str


class ApplicationResultRequest (BaseModel) :
    student_id: str = Field(..., description = "학번")
    phone_number: str = Field(..., description = "전화번호")
    name: str = Field(..., description = "이름")


class ApplicationResultResponse (BaseModel) :
    message: str
    status: str
