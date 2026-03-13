"""
seed_data.py — Run this script ONCE to populate demo data.

Usage:
    python manage.py shell < seed_data.py
OR (from project root):
    python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_nova.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import StudentProfile, TeacherProfile, Subject, CareerPath

print("🌱 Seeding CareerNova demo data...")

# ── Superadmin ──
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin', email='admin@careernova.edu',
        password='admin123', first_name='Admin', last_name='User'
    )
    print("✅ Created superadmin — admin / admin123")
else:
    admin = User.objects.get(username='admin')
    print("⚠️  Admin already exists, skipping.")

# ── Demo Teacher ──
if not User.objects.filter(username='teacher_demo').exists():
    t_user = User.objects.create_user(
        username='teacher_demo', email='teacher@careernova.edu',
        password='teacher123', first_name='Prof. Ramesh', last_name='Kumar',
        is_staff=True,
    )
    TeacherProfile.objects.create(
        user=t_user, department='Computer Science', employee_id='TCH2024001'
    )
    print("✅ Created teacher — teacher_demo / teacher123")
else:
    print("⚠️  Teacher already exists, skipping.")

# ── Demo students ──
students_data = [
    {
        'username': 'arjun_sharma',
        'first_name': 'Arjun',
        'last_name': 'Sharma',
        'roll': 'CS2021042',
        'dept': 'Computer Science',
        'semester': 5,
        'cgpa': 8.4,
        'attendance': 82.0,
        'risk': 'Low',
        'subjects': [
            ('Data Structures', 88, 100),
            ('Operating Systems', 79, 100),
            ('DBMS', 85, 100),
            ('Machine Learning', 74, 100),
            ('Computer Networks', 80, 100),
        ],
        'careers': [
            ('Full Stack Engineer', 'Build end-to-end web applications at top product companies leveraging your strong DSA and web dev skills.', 94),
            ('ML/AI Engineer', 'Apply ML fundamentals to build intelligent systems and data pipelines for large-scale applications.', 82),
            ('Cloud Solutions Architect', 'Design scalable cloud infrastructure using AWS/GCP/Azure combining your database and networking knowledge.', 71),
        ]
    },
    {
        'username': 'priya_patel',
        'first_name': 'Priya',
        'last_name': 'Patel',
        'roll': 'CS2021019',
        'dept': 'Computer Science',
        'semester': 5,
        'cgpa': 7.1,
        'attendance': 68.0,
        'risk': 'Medium',
        'subjects': [
            ('Data Structures', 65, 100),
            ('Operating Systems', 58, 100),
            ('DBMS', 71, 100),
            ('Machine Learning', 62, 100),
            ('Computer Networks', 70, 100),
        ],
        'careers': [
            ('Frontend Developer', 'Focus on UI/UX and JavaScript frameworks to build user-facing products.', 78),
            ('Data Analyst', 'Leverage your DBMS skills for business intelligence and reporting roles.', 72),
            ('QA Engineer', 'Systematic testing and quality assurance for software products.', 65),
        ]
    },
    {
        'username': 'rohan_mehta',
        'first_name': 'Rohan',
        'last_name': 'Mehta',
        'roll': 'CS2021033',
        'dept': 'Computer Science',
        'semester': 5,
        'cgpa': 5.8,
        'attendance': 51.0,
        'risk': 'High',
        'subjects': [
            ('Data Structures', 45, 100),
            ('Operating Systems', 52, 100),
            ('DBMS', 48, 100),
            ('Machine Learning', 40, 100),
            ('Computer Networks', 55, 100),
        ],
        'careers': [
            ('IT Support Specialist', 'Foundational IT skills can lead to system administration and helpdesk roles.', 60),
            ('Technical Recruiter', 'Use domain knowledge to identify and assess technical talent.', 55),
            ('Junior Developer', 'Start with internships to build practical coding skills step-by-step.', 50),
        ]
    },
    {
        'username': 'sneha_reddy',
        'first_name': 'Sneha',
        'last_name': 'Reddy',
        'roll': 'CS2021007',
        'dept': 'Computer Science',
        'semester': 5,
        'cgpa': 9.1,
        'attendance': 93.0,
        'risk': 'Low',
        'subjects': [
            ('Data Structures', 95, 100),
            ('Operating Systems', 89, 100),
            ('DBMS', 92, 100),
            ('Machine Learning', 88, 100),
            ('Computer Networks', 90, 100),
        ],
        'careers': [
            ('Software Engineer at FAANG', 'Exceptional academic performance opens doors to top-tier tech companies.', 97),
            ('Research Scientist', 'Strong theoretical foundations suit AI/ML research at companies like DeepMind.', 91),
            ('Product Manager', 'Combine technical depth with strategic thinking for PM roles at top companies.', 83),
        ]
    },
]

for sdata in students_data:
    if User.objects.filter(username=sdata['username']).exists():
        print(f"⚠️  Student {sdata['username']} already exists, skipping.")
        continue

    user = User.objects.create_user(
        username=sdata['username'],
        password='student123',
        first_name=sdata['first_name'],
        last_name=sdata['last_name'],
        email=f"{sdata['username']}@college.edu"
    )

    profile = StudentProfile.objects.create(
        user=user,
        roll_number=sdata['roll'],
        department=sdata['dept'],
        semester=sdata['semester'],
        cgpa=sdata['cgpa'],
        attendance=sdata['attendance'],
        risk_level=sdata['risk'],
    )

    for subj_name, obtained, max_m in sdata['subjects']:
        Subject.objects.create(
            student=profile,
            name=subj_name,
            marks_obtained=obtained,
            max_marks=max_m
        )

    for career_title, career_desc, match in sdata['careers']:
        CareerPath.objects.create(
            student=profile,
            title=career_title,
            description=career_desc,
            match_score=match
        )

    print(f"✅ Created student: {sdata['first_name']} {sdata['last_name']} ({sdata['roll']}) — Risk: {sdata['risk']}")

print("\n🎉 Seed complete!")
print("\nLogin credentials:")
print("  Superadmin  → admin        / admin123")
print("  Teacher     → teacher_demo / teacher123")
print("  Student     → arjun_sharma / student123")
print("  Student     → sneha_reddy  / student123")
print("\nRun server: python manage.py runserver")
