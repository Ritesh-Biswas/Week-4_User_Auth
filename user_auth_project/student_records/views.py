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
            print("Admin logged in, session:", request.session.items())
            return redirect("admin_dashboard")  # Redirect to admin dashboard
        except Admin.DoesNotExist:
            pass

        # Check if the user is a student
        try:
            student = Student.objects.get(username=username, password=password)
            request.session["username"] = student.username  # Set the username here!
            request.session["user_role"] = "student"
            request.session["user_id"] = student.id
            print("Student logged in, session:", list(request.session.items()))
            return redirect("student_dashboard")
        except Student.DoesNotExist:
            pass

        # If authentication fails:
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

def admin_student_edit(request, student_id):
    # Check if the user is logged in as admin
    if request.session.get("user_role") != "admin":
        return redirect("login")

    # Fetch the student record by ID
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect("admin_student_list")

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.section = request.POST.get("section")
        student.email = request.POST.get("email")
        # Note: Username and password are not updated via this form
        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect("admin_student_list")

    return render(request, "admin_student_edit.html", {"student": student})


def admin_student_delete(request, student_id):
    # Check if the user is logged in as admin
    if request.session.get("user_role") != "admin":
        return redirect("login")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect("admin_student_list")

    # Delete the student record
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect("admin_student_list")


def student_profile_edit(request):
    # Print the session items for debugging
    print("In student_profile_edit, session:", list(request.session.items()))
    
    # Check if the user is logged in as student
    if request.session.get("user_role") != "student":
        print("User is not recognized as student, redirecting to login.")
        return redirect("login")
    
    username = request.session.get("username")
    if not username:
        print("No username found in session, redirecting to login.")
        return redirect("login")
    
    try:
        student = Student.objects.get(username=username)
    except Student.DoesNotExist:
        print(f"Student with username {username} not found.")
        messages.error(request, "Student not found.")
        return redirect("login")
    
    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        password = request.POST.get("password")
        if password:
            student.password = password
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("student_profile_edit")
    
    return render(request, "student_profile_edit.html", {"student": student})



