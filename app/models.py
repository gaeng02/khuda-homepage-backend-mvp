from sqlalchemy import BigInteger, Boolean, Column, Enum, Integer, Text, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

ApplicantType = Enum("yb", "ob", name="applicant_type_enum")
QuestionAudience = Enum("common", "yb", "ob", name="question_audience_enum")
ApplicationStatus = Enum("submitted", "reviewing", "accepted", "rejected", name="application_status_enum")


class Applications (Base) :
    
    __tablename__ = "applications"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    applicant_type = Column(ApplicantType, nullable=False)
    answers = Column(JSONB, nullable=False)
    status = Column(ApplicationStatus, nullable=False, server_default="submitted")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class Questions (Base) :
    __tablename__ = "questions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    applicant_type = Column(QuestionAudience, nullable=False)
    field_type = Column(String(32), nullable=False)
    required = Column(Boolean, nullable=False, server_default="true")
    max_len = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
