# IT Help Desk Management System

A web-based IT Help Desk application built with Python and Flask. It allows users to submit technical support tickets and enables administrators to manage, search, track, and resolve reported issues.

## Features

- Submit IT support tickets.
- Store tickets in an SQLite database.
- Admin login and logout.
- Protected administrative dashboard.
- Search tickets by name, email, category, priority, or description.
- Track ticket statuses: Open, In Progress, and Resolved.
- Add resolution notes to tickets.
- Dashboard statistics showing ticket totals and statuses.
- Password hashing for admin authentication.
- CSRF protection for form submissions.
- Environment-based configuration for credentials and secret keys.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Flask-WTF
- Werkzeug

## Installation

1. Clone or download this repository.
2. Open the project folder in your terminal.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Configure the required environment variables before starting the application.

5. Run the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## Project Structure

```text
it-helpdesk-system/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
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

This project demonstrates practical skills in backend development, database management, web application development, authentication, and basic application security.