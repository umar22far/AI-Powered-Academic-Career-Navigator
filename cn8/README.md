# 🚀 CareerNova — AI-Powered Academic & Career Navigator

A hackathon Django web application for Hawkathon 2026.

---

## 📁 Project Structure

```
careernova/
│
├── manage.py                    # Django entry point
├── db.sqlite3                   # SQLite database (auto-created)
├── seed_data.py                 # Demo data population script
│
├── career_nova/                 # Django project settings package
│   ├── __init__.py
│   ├── settings.py              # All Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                        # Main app
│   ├── __init__.py
│   ├── models.py                # StudentProfile, Subject, CareerPath models
│   ├── views.py                 # All 4 page views (function-based)
│   ├── urls.py                  # App URL patterns
│   ├── admin.py                 # Admin panel registration
│   └── apps.py
│
├── templates/                   # HTML templates
│   ├── login.html               # Page 1 — Login
│   ├── dashboard.html           # Page 2 — Main Dashboard
│   ├── student_dashboard.html   # Page 3 — Student Dashboard
│   └── teacher_dashboard.html   # Page 4 — Teacher Dashboard
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

---

## ⚙️ Installation & Setup

### Step 1 — Install Python & Django

```bash
pip install django
```

### Step 2 — Navigate to project directory

```bash
cd careernova
```

### Step 3 — Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4 — Populate demo data

```bash
python seed_data.py
```

This creates:
- Admin user: `admin` / `admin123`
- 4 demo students with subjects and AI career paths

### Step 5 — Run the server

```bash
python manage.py runserver
```

---

## 🌐 Pages & URLs

| Page | URL | Description |
|------|-----|-------------|
| Login | `/login/` | Login with username + password |
| Main Dashboard | `/dashboard/` | Overview stats, portals, recent students |
| Student Dashboard | `/student/` | Profile, skills, grades, AI career paths |
| Teacher Dashboard | `/teacher/` | All students, risk levels, analytics |
| Admin Panel | `/admin/` | Full data management |

---

## 👤 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin/Teacher | `admin` | `admin123` |
| Student | `arjun_sharma` | `student123` |
| Student | `sneha_reddy` | `student123` |

---

## ✨ Features

- 🔐 Session-based Django login
- 📊 Animated circular progress bars (Canvas API)
- 🎨 Modern dark UI with gradient accents
- 📱 Responsive design
- 🤖 Demo AI career path cards
- ⚠️ Risk level classification (Low/Medium/High)
- 🔍 Live search + filter on Teacher Dashboard
- 👑 Full Django Admin panel

---

## 🛠 Tech Stack

- **Backend**: Django 4.x (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite3
- **Fonts**: Syne + DM Sans (Google Fonts)
