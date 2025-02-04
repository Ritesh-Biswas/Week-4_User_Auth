from django.core.management.base import BaseCommand # type: ignore
from student_records.models import Admin, Student
from django.db.utils import IntegrityError # type: ignore

class Command(BaseCommand):
    help = "Seed the database with dummy admin and student data"

    def handle(self, *args, **kwargs):
        # Create default admin
        try:
            Admin.objects.create(
                username="admin",
                name="Default Admin",
                email="admin@example.com",
                password="admin123",
                role="admin",
            )
            self.stdout.write(self.style.SUCCESS("Successfully created the default admin!"))
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Default admin already exists."))

        # Seed student data
        students = [
            {"username": "student1", "name": "Alice", "email": "alice@example.com", "section": "A", "password": "password1"},
            {"username": "student2", "name": "Bob", "email": "bob@example.com", "section": "B", "password": "password2"},
            {"username": "student3", "name": "Charlie", "email": "charlie@example.com", "section": "A", "password": "password3"},
        ]

        for student in students:
            Student.objects.update_or_create(
                username=student["username"],
                defaults=student,
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with students!"))
