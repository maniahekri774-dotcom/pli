"""Student profile model."""

from datetime import datetime
from app.extensions import db


class Student(db.Model):
    """Extended profile data for users with the 'student' role."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    student_code = db.Column(db.String(20), unique=True, nullable=False)
    national_id = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    address = db.Column(db.String(255))
    guardian_name = db.Column(db.String(120))
    guardian_phone = db.Column(db.String(20))
    current_level = db.Column(db.String(30))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    submissions = db.relationship("Submission", back_populates="student", cascade="all, delete-orphan")
    attendances = db.relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    certificates = db.relationship("Certificate", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.student_code}>"
