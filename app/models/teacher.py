"""Teacher profile model."""

from datetime import datetime
from app.extensions import db


class Teacher(db.Model):
    """Extended profile data for users with the 'teacher' role."""

    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    teacher_code = db.Column(db.String(20), unique=True, nullable=False)
    bio = db.Column(db.Text)
    specialization = db.Column(db.String(120))
    years_experience = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="teacher_profile")
    courses = db.relationship("Course", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher {self.teacher_code}>"
