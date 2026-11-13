# IT Help Desk Management System

A web-based IT Help Desk Management System built with Python, Flask, and SQLite. The application allows users to submit technical support tickets while administrators can manage, track, search, and resolve reported issues through a secure dashboard.

## Features

- Submit technical support tickets.
- Store submitted tickets in an SQLite database.
- Secure admin login and logout.
- Protected administrative dashboard.
- Search tickets by name, email, category, priority, or description.
- Track ticket statuses: Open, In Progress, and Resolved.
- Add resolution notes to tickets.
- View dashboard statistics.
- Password hashing for admin authentication.
- CSRF protection for form submissions.
- Environment-based configuration for sensitive credentials.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Flask-WTF
- Werkzeug

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/semiloree14/it-helpdesk-system.git
```

### 2. Navigate into the project directory

```bash
cd it-helpdesk-system
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

In PowerShell, set the following variables:

```powershell
$env:SECRET_KEY="your-secret-key"
$env:ADMIN_USERNAME="admin"
$env:ADMIN_PASSWORD_HASH="your-password-hash"
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate an admin password hash with:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

Replace the example values with your own. Never publish your actual secrets or password hash.

### 5. Run the application

```bash
python app.py
```

### 6. Open the application

Visit:

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically when the application starts.

## Project Structure

```text
it-helpdesk-system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── ticket.html
│   ├── login.html
│   └── dashboard.html
│
└── static/
    └── style.css
```

## Purpose

This project demonstrates practical skills in Python backend development, database management, web application development, authentication, and application security.