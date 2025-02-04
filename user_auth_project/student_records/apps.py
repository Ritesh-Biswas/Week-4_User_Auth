from django.apps import AppConfig # type: ignore
from django.db.utils import IntegrityError # type: ignore


class StudentRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_records'
    
def ready(self):
    from .models import Admin
    try:
        Admin.objects.create(username="admin", name="Default Admin", email="admin@example.com", password="admin123")
    except IntegrityError:
        pass
