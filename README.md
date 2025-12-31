User Management System (Django)

## 📌 Project Overview
This project is a User Management System built using Django REST Framework (DRF) for the Backend Developer Intern assessment.  
It provides secure RESTful APIs for user registration, authentication using JWT, profile management, and password updates.

The project focuses on authentication flows, API security, role-based access control (RBAC), and clean backend architecture.

---

##  Features
- User registration
- JWT-based authentication
- Protected API endpoints
- View user profile
- Change password
- Role-based access control (RBAC)
- Environment-based configuration
- Cloud deployment

---

##  Tech Stack

### Backend
- Django
- Django REST Framework (DRF)
- JWT Authentication (SimpleJWT)
- PostgreSQL
- Django ORM

### Frontend
- React
- JavaScript
- HTML
- CSS

### Tools & Platforms
- Git & GitHub
- Render (Backend)
- Vercel (Frontend)
- Postman (API Testing)

---

##  Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
---

### Frontend
- React
- JavaScript
- HTML, CSS
---

### Tools & Platforms
- Git & GitHub
- Render (Backend Deployment)
- Vercel (Frontend Deployment)
- Postman (API Testing & Documentation)
---

##  Project Structure
backend-intern-assessment/
│
├── frontend/
│ ├── src/
│ ├── package.json
│ └── vite.config.js
│
├── backend/
│ ├── user_management/
│ ├── users/
│ ├── manage.py
│ ├── requirements.txt
│ └── tests/
│
├── README.md
├── .gitignore



---

##  Setup Instructions (Local Development)

###  Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Git

---


```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
---

###  Frontend Setup 

cd frontend
npm install
npm run dev
---
## Environment Variables
SECRET_KEY = 'django-insecure-c0d(=9hk)!8e2da&aa2!&9z!b=*rbhc!zszzyzbi*0we^hof!9'
---

### Deployment Instructions
##Backend Deployment

Backend is deployed on Render
PostgreSQL database is cloud-hosted (Render / Neon)
Environment variables configured via Render dashboard
Static files handled by Render
APIs accessible via public endpoints

##Frontend Deployment

Frontend is deployed on Vercel
Backend API base URL configured via environment variables
Automatic build and deployment
---
###Testing

Basic unit tests written using Django TestCase
Tests can be run using: python manage.py test

---
###Live Deployment Links

Frontend URL: https://user-management-frontend-kbxa3l4jb-jagans-projects-cdd588e0.vercel.app/login
Backend API URL: https://user-management-backend-h543.onrender.com/
-----------------------------------------------------


