"""Attendance model."""

from datetime import datetime
from app.extensions import db


class Attendance(db.Model):
    """Per-session attendance record for a student in a course."""

    __tablename__ = "attendances"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    session_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(15), nullable=False)  # present, absent, late, excused
    note = db.Column(db.String(255))

    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("Student", back_populates="attendances")
    course = db.relationship("Course")

    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", "session_date", name="uq_attendance_session"),
    )

    def __repr__(self):
        return f"<Attendance {self.student_id} {self.session_date} {self.status}>"
