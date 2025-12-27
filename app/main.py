from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db, engine, SessionLocal
from app.models import Base, Applications, Questions
from app.schemas import ApplicationCreate, ApplicationCreated, QuestionsResponse
from app.seed import seed_questions


def validate_answers(applicant_type: str, questions: list[Questions], answers: dict[str, str]):
    for q in questions:
        key = str(q.id)
        val = answers.get(key)

        if q.required and (val is None or str(val).strip() == ""):
            raise HTTPException(status_code=400, detail=f"required: question_id={q.id}")

        if val is None:
            continue

        if q.field_type in ("text", "textarea"):
            s = str(val)
            if q.max_len is not None and len(s) > q.max_len:
                raise HTTPException(status_code=400, detail=f"max_len: question_id={q.id}")

    allowed_ids = {str(q.id) for q in questions}
    unknown = [k for k in answers.keys() if k not in allowed_ids]
    if unknown:
        raise HTTPException(status_code=400, detail=f"unknown_question_ids: {unknown}")


def main() :
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db :
        seed_questions(db)

    app = FastAPI()

    @app.get("/api/questions/{applicant_type}", response_model=QuestionsResponse)
    def get_questions (applicant_type: str, db: Session = Depends(get_db)) :
        if applicant_type not in ("yb", "ob"):
            raise HTTPException(status_code=404, detail="invalid applicant_type")

        qs = (
            db.query(Questions)
            .filter(Questions.applicant_type.in_(["common", applicant_type]))
            .order_by(Questions.position.asc(), Questions.id.asc())
            .all()
        )

        return {
            "applicant_type": applicant_type,
            "questions": [
                {
                    "id": q.id,
                    "question": q.question,
                    "applicant_type": q.applicant_type,
                    "field_type": q.field_type,
                    "required": q.required,
                    "max_len": q.max_len,
                    "position": q.position,
                }
                for q in qs
            ],
        }

    @app.post("/api/applications", response_model=ApplicationCreated)
    def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
        applicant_type = payload.applicant_type
        qs = (
            db.query(Questions)
            .filter(Questions.applicant_type.in_(["common", applicant_type]))
            .order_by(Questions.position.asc(), Questions.id.asc())
            .all()
        )

        validate_answers(applicant_type, qs, payload.answers)

        app_row = Applications(applicant_type=applicant_type, answers=payload.answers, status="submitted")
        db.add(app_row)
        db.commit()
        db.refresh(app_row)

        return {"application_id": app_row.id, "status": app_row.status}

    return app


app = main()
