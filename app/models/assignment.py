"""Assignment and Submission models."""

from datetime import datetime
from app.extensions import db


class Assignment(db.Model):
    """Homework/assignment created by a teacher for a course."""

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    attachment_url = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)
    max_score = db.Column(db.Integer, default=100)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    course = db.relationship("Course", back_populates="assignments")
    submissions = db.relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assignment {self.title}>"


class Submission(db.Model):
    """A student's submission for an assignment."""

    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    file_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    graded_at = db.Column(db.DateTime)

    assignment = db.relationship("Assignment", back_populates="submissions")
    student = db.relationship("Student", back_populates="submissions")

    __table_args__ = (db.UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student"),)

    def __repr__(self):
        return f"<Submission assignment={self.assignment_id} student={self.student_id}>"
