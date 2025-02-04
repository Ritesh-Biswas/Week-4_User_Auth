from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin/students/", views.admin_student_list, name="admin_student_list"),

]
