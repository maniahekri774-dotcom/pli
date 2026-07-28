"""Grade and Certificate models."""

from datetime import datetime
from app.extensions import db


class Grade(db.Model):
    """Final grade for a student in a course."""

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    score = db.Column(db.Numeric(5, 2))
    letter_grade = db.Column(db.String(5))
    comments = db.Column(db.Text)

    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("Student", back_populates="grades")
    course = db.relationship("Course")

    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_grade_student_course"),)

    def __repr__(self):
        return f"<Grade {self.student_id} {self.course_id} {self.score}>"


class Certificate(db.Model):
    """Completion certificate issued to a student."""

    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    file_url = db.Column(db.String(255))
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("Student", back_populates="certificates")
    course = db.relationship("Course")

    def __repr__(self):
        return f"<Certificate {self.certificate_number}>"
