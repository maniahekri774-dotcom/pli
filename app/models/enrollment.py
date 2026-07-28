"""Enrollment and Payment models."""

from datetime import datetime
from app.extensions import db


class Enrollment(db.Model):
    """Links a student to a course."""

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    status = db.Column(db.String(20), default="pending", nullable=False)  # pending, active, completed, cancelled
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    payment = db.relationship("Payment", back_populates="enrollment", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),)

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id}>"


class Payment(db.Model):
    """Payment record for an enrollment."""

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), unique=True, nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default="IRR")
    method = db.Column(db.String(30))  # card, cash, online_gateway
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending, paid, failed, refunded
    transaction_ref = db.Column(db.String(120))
    paid_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    enrollment = db.relationship("Enrollment", back_populates="payment")

    def __repr__(self):
        return f"<Payment {self.id} status={self.status}>"
