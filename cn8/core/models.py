from django.db import models
from django.contrib.auth.models import User


class TeacherProfile(models.Model):
    """Stores extra info about a teacher."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, default='Computer Science')
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()} ({self.employee_id})"


class StudentProfile(models.Model):
    """Stores extra info about a student beyond the default Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default='Computer Science')
    semester = models.IntegerField(default=1)
    cgpa = models.FloatField(default=0.0)
    attendance = models.FloatField(default=0.0)   # percentage 0-100
    risk_level = models.CharField(
        max_length=20,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Low'
    )
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class Subject(models.Model):
    """A subject/course a student is enrolled in."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    marks_obtained = models.FloatField(default=0.0)
    max_marks = models.FloatField(default=100.0)

    def percentage(self):
        if self.max_marks == 0:
            return 0
        return round((self.marks_obtained / self.max_marks) * 100, 1)

    def __str__(self):
        return f"{self.name} — {self.student}"


class CareerPath(models.Model):
    """AI-generated career path for a student."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='career_paths')
    title = models.CharField(max_length=200)
    description = models.TextField()
    match_score = models.IntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.student}"
