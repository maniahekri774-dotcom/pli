"""Model registry — import all models here so Flask-Migrate detects them."""

from app.models.user import User, Role
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course, Category
from app.models.enrollment import Enrollment, Payment
from app.models.assignment import Assignment, Submission
from app.models.attendance import Attendance
from app.models.grade import Grade, Certificate
from app.models.content import BlogPost, Page, FAQ, Testimonial, Event, GalleryItem
from app.models.message import Message, Announcement, Notification
from app.models.contact import ContactSubmission
from app.models.audit import AuditLog

__all__ = [
    "User", "Role", "Student", "Teacher", "Course", "Category",
    "Enrollment", "Payment", "Assignment", "Submission", "Attendance",
    "Grade", "Certificate", "BlogPost", "Page", "FAQ", "Testimonial",
    "Event", "GalleryItem", "Message", "Announcement", "Notification",
    "ContactSubmission", "AuditLog",
]
