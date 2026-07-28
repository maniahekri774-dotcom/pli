"""Course, Category, and Level models."""

from datetime import datetime
from app.extensions import db


class Category(db.Model):
    """Course category, e.g. General Persian, Business Persian, Exam Prep."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    courses = db.relationship("Course", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Course(db.Model):
    """A course offering."""

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    summary = db.Column(db.String(300))
    description = db.Column(db.Text)
    level = db.Column(db.String(30))
    cover_image = db.Column(db.String(255))

    price = db.Column(db.Numeric(10, 2), default=0)
    discount_price = db.Column(db.Numeric(10, 2))
    duration_weeks = db.Column(db.Integer)
    capacity = db.Column(db.Integer, default=20)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="courses")

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher", back_populates="courses")

    is_published = db.Column(db.Boolean, default=False, nullable=False)
    starts_at = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    @property
    def seats_taken(self):
        return sum(1 for e in self.enrollments if e.status == "active")

    def __repr__(self):
        return f"<Course {self.title}>"
