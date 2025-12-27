from sqlalchemy.orm import Session

from app.models import Questions


def seed_questions(db: Session):
    existing = db.query(Questions).count()
    if existing > 0:
        return

    items = [
        Questions(
            applicant_type="common",
            position=10,
            field_type="text",
            required=True,
            max_len=50,
            question="이름을 입력해주세요."
        ),
        Questions(
            applicant_type="common",
            position=20,
            field_type="text",
            required=True,
            max_len=100,
            question="이메일을 입력해주세요."
        ),
        Questions(
            applicant_type="yb",
            position=30,
            field_type="textarea",
            required=True,
            max_len=2000,
            question="지원동기를 적어주세요."
        ),
        Questions(
            applicant_type="ob",
            position=30,
            field_type="textarea",
            required=True,
            max_len=2000,
            question="경력/활동 내용을 포함해 지원동기를 적어주세요."
        ),
    ]

    db.add_all(items)
    db.commit()
