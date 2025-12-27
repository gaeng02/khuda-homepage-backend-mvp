from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


ApplicantType = Literal["yb", "ob"]
AudienceType = Literal["common", "yb", "ob"]


class QuestionOut (BaseModel) :
    id: int
    question: str
    applicant_type: AudienceType
    field_type: str
    required: bool
    max_len: Optional[int] = None
    min_len: Optional[int] = None
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
