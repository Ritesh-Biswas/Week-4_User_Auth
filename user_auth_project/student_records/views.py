from django.shortcuts import render, redirect # type: ignore
from student_records.models import Admin, Student
from django.contrib import messages # type: ignore

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if the user is an admin
        try:
            admin = Admin.objects.get(username=username, password=password)
            request.session["user_role"] = "admin"
            request.session["user_id"] = admin.id
            return redirect("admin_dashboard")  # Redirect to admin dashboard
        except Admin.DoesNotExist:
            pass

        # Check if the user is a student
        try:
            student = Student.objects.get(username=username, password=password)
            request.session["user_role"] = "student"
            request.session["user_id"] = student.id
            return redirect("student_dashboard")  # Redirect to student dashboard
        except Student.DoesNotExist:
            pass

        # Invalid credentials
        return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


def admin_dashboard(request):
    if request.session.get("user_role") != "admin":
        return redirect("login")
    return render(request, "admin_dashboard.html")

def student_dashboard(request):
    if request.session.get("user_role") != "student":
        return redirect("login")
    return render(request, "student_dashboard.html")

def admin_student_list(request):
    # Check if the user is logged in as admin
    if request.session.get("user_role") != "admin":
        return redirect("login")

    # Fetch all students from the database
    students = Student.objects.all()
    return render(request, "admin_student_list.html", {"students": students})


def admin_student_add(request):
    # Check if the user is logged in as admin
    if request.session.get("user_role") != "admin":
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        section = request.POST.get("section")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if Student.objects.filter(username=username).exists():
            messages.error(request, "A student with this username already exists.")
        else:
            # Create a new student
            Student.objects.create(username=username, name=name, section=section, email=email, password=password)
            messages.success(request, "Student added successfully!")
            return redirect("admin_student_list")

    return render(request, "admin_student_add.html")