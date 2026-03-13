"""
CareerNova — Views with role-based access control.
Roles: student (StudentProfile) | teacher (TeacherProfile) | admin (is_staff)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import StudentProfile, TeacherProfile, Subject, CareerPath

# ML predictor
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ml.predictor import predict_student


# ── helpers ──────────────────────────────────
def is_teacher(user):
    return user.is_staff or hasattr(user, 'teacherprofile')

def is_student(user):
    return hasattr(user, 'studentprofile')


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return _role_redirect(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return _role_redirect(user)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def _role_redirect(user):
    """Send each role to the right page after login."""
    if is_teacher(user):
        return redirect('teacher')
    elif is_student(user):
        return redirect('student')
    else:
        return redirect('dashboard')


# ──────────────────────────────────────────────
# SIGNUP
# ──────────────────────────────────────────────
def signup_view(request):
    if request.user.is_authenticated:
        return _role_redirect(request.user)

    if request.method == 'POST':
        role        = request.POST.get('role', 'student')
        first_name  = request.POST.get('first_name', '').strip()
        last_name   = request.POST.get('last_name', '').strip()
        username    = request.POST.get('username', '').strip()
        email       = request.POST.get('email', '').strip()
        department  = request.POST.get('department', 'Computer Science').strip()
        password1   = request.POST.get('password1', '').strip()
        password2   = request.POST.get('password2', '').strip()

        # Student-specific
        roll_number = request.POST.get('roll_number', '').strip()
        semester    = request.POST.get('semester', '1').strip()

        # Teacher-specific
        employee_id = request.POST.get('employee_id', '').strip()

        if not all([first_name, username, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')

        if role == 'student':
            if not roll_number:
                messages.error(request, 'Roll number is required for students.')
                return render(request, 'signup.html')
            if StudentProfile.objects.filter(roll_number=roll_number).exists():
                messages.error(request, 'Roll number already registered.')
                return render(request, 'signup.html')
        else:
            if not employee_id:
                messages.error(request, 'Employee ID is required for teachers.')
                return render(request, 'signup.html')
            if TeacherProfile.objects.filter(employee_id=employee_id).exists():
                messages.error(request, 'Employee ID already registered.')
                return render(request, 'signup.html')

        user = User.objects.create_user(
            username=username, email=email, password=password1,
            first_name=first_name, last_name=last_name,
        )

        if role == 'student':
            StudentProfile.objects.create(
                user=user, roll_number=roll_number,
                department=department,
                semester=int(semester) if semester.isdigit() else 1,
            )
        else:
            # Teachers get staff status so they can access Django admin
            user.is_staff = True
            user.save()
            TeacherProfile.objects.create(
                user=user, department=department, employee_id=employee_id,
            )

        login(request, user)
        messages.success(request, f'Welcome to CareerNova, {first_name}!')
        return _role_redirect(user)

    return render(request, 'signup.html')


# ──────────────────────────────────────────────
# LOGOUT
# ──────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('login')


# ──────────────────────────────────────────────
# OVERVIEW DASHBOARD (admin/superuser only)
# ──────────────────────────────────────────────
@login_required
def dashboard_view(request):
    if not request.user.is_superuser:
        return _role_redirect(request.user)

    total_students  = StudentProfile.objects.count()
    high_risk       = StudentProfile.objects.filter(risk_level='High').count()
    medium_risk     = StudentProfile.objects.filter(risk_level='Medium').count()
    low_risk        = StudentProfile.objects.filter(risk_level='Low').count()
    recent_students = StudentProfile.objects.select_related('user').order_by('-id')[:5]

    context = {
        'total_students': total_students,
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        'recent_students': recent_students,
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


# ──────────────────────────────────────────────
# STUDENT PORTAL — students only
# ──────────────────────────────────────────────
@login_required
def student_dashboard_view(request):
    if not is_student(request.user):
        messages.error(request, 'Access denied. This portal is for students only.')
        return redirect('teacher') if is_teacher(request.user) else redirect('login')

    profile      = request.user.studentprofile
    subjects     = profile.subjects.all()

    # ── Run ML prediction and update profile ──
    marks = [s.marks_obtained for s in subjects]
    if marks:
        result = predict_student(marks)
        # Update risk level from ML model
        if profile.risk_level != result['risk_level']:
            profile.risk_level = result['risk_level']
            profile.save()
        # Refresh career paths from ML suggestions
        profile.career_paths.all().delete()
        for title, desc, score in result['careers']:
            CareerPath.objects.create(
                student=profile, title=title,
                description=desc, match_score=score
            )
        ml_tier = result['tier']
    else:
        ml_tier = None

    career_paths = profile.career_paths.all()

    context = {
        'profile':      profile,
        'subjects':     subjects,
        'career_paths': career_paths,
        'ml_tier':      ml_tier,
        'user':         request.user,
    }
    return render(request, 'student_dashboard.html', context)


# ──────────────────────────────────────────────
# TEACHER DASHBOARD — teachers + admins only
# ──────────────────────────────────────────────
@login_required
def teacher_dashboard_view(request):
    if not is_teacher(request.user):
        messages.error(request, 'Access denied. This dashboard is for teachers only.')
        return redirect('student') if is_student(request.user) else redirect('login')

    all_students = StudentProfile.objects.select_related('user').prefetch_related('subjects').all()
    total        = all_students.count()
    avg_cgpa = avg_attendance = 0
    if total > 0:
        avg_cgpa       = round(sum(s.cgpa for s in all_students) / total, 2)
        avg_attendance = round(sum(s.attendance for s in all_students) / total, 1)

    context = {
        'all_students': all_students,
        'total': total,
        'avg_cgpa': avg_cgpa,
        'avg_attendance': avg_attendance,
        'high_risk_count': all_students.filter(risk_level='High').count(),
        'user': request.user,
        'is_teacher': True,
    }
    return render(request, 'teacher_dashboard.html', context)


# ──────────────────────────────────────────────
# EDIT STUDENT — teachers + admins only
# ──────────────────────────────────────────────
@login_required
def edit_student_view(request, student_id):
    if not is_teacher(request.user):
        messages.error(request, 'Access denied.')
        return redirect('login')

    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        student.cgpa       = float(request.POST.get('cgpa', student.cgpa))
        student.attendance = float(request.POST.get('attendance', student.attendance))
        student.semester   = int(request.POST.get('semester', student.semester))
        student.department = request.POST.get('department', student.department)

        # Re-run ML on current subject marks to update risk level
        marks = [s.marks_obtained for s in student.subjects.all()]
        if marks:
            result = predict_student(marks)
            student.risk_level = result['risk_level']
            # Refresh career paths
            student.career_paths.all().delete()
            for title, desc, score in result['careers']:
                CareerPath.objects.create(
                    student=student, title=title,
                    description=desc, match_score=score
                )
        else:
            student.risk_level = request.POST.get('risk_level', student.risk_level)

        student.save()
        messages.success(request, f"{student.user.get_full_name()}'s profile updated.")
        return redirect('teacher')

    context = {'student': student, 'user': request.user}
    return render(request, 'edit_student.html', context)
