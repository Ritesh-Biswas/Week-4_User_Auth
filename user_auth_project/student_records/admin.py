from django.contrib import admin # type: ignore
from .models import Admin, Student

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "email", "role")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "email", "section")
