from django.urls import path # type: ignore
from django.shortcuts import redirect # type: ignore
from . import views

def root_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path("login/", views.login_view, name="login"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin/students/", views.admin_student_list, name="admin_student_list"),
    path("admin/students/add/", views.admin_student_add, name="admin_student_add"),
    path("admin/students/edit/<int:student_id>/", views.admin_student_edit, name="admin_student_edit"),
    path("admin/students/delete/<int:student_id>/", views.admin_student_delete, name="admin_student_delete"),

]
