# 🚀 CareerNova — How to Run in VS Code

## Step-by-Step Setup

### 1. Open the folder in VS Code
File → Open Folder → select the `careernova` folder (the one with `manage.py` inside)

### 2. Open the terminal inside VS Code
Press `Ctrl + `` ` (backtick) to open the integrated terminal

### 3. Create a virtual environment
```bash
python -m venv venv
```

### 4. Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```
**Mac / Linux:**
```bash
source venv/bin/activate
```
You'll see `(venv)` appear at the start of your terminal line.

### 5. Install Django
```bash
pip install django
```

### 6. Select the Python interpreter in VS Code
- Press `Ctrl + Shift + P`
- Type: `Python: Select Interpreter`
- Choose the one that shows `venv` in its path

### 7. Run migrations (sets up the database)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Seed demo data (creates users + sample students)
```bash
python seed_data.py
```

### 9. Start the server
```bash
python manage.py runserver
```

### 10. Open in browser
Go to: http://127.0.0.1:8000/

---

## Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin / Teacher | `admin` | `admin123` |
| Student | `arjun_sharma` | `student123` |
| Student | `sneha_reddy` | `student123` |

---

## Pages

| Page | URL |
|------|-----|
| Login | http://127.0.0.1:8000/login/ |
| Main Dashboard | http://127.0.0.1:8000/dashboard/ |
| Student Portal | http://127.0.0.1:8000/student/ |
| Teacher Dashboard | http://127.0.0.1:8000/teacher/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

---

## How the URL → View → Template flow works

```
urls.py                views.py              templates/
-------                --------              ----------
path('dashboard/', --> dashboard_view() --> render(request, 'dashboard.html', context)
path('student/',   --> student_dashboard_view() --> 'student_dashboard.html'
path('teacher/',   --> teacher_dashboard_view() --> 'teacher_dashboard.html'
path('login/',     --> login_view()       --> 'login.html'
```

In your HTML templates, links use Django's `{% url %}` tag:
```html
<a href="{% url 'dashboard' %}">Go to Dashboard</a>
<a href="{% url 'student' %}">Student Portal</a>
<a href="{% url 'logout' %}">Logout</a>
```

This way, if you ever change a URL path in `urls.py`, the links in HTML update automatically.
