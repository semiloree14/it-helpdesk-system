
import os
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import check_password_hash
from flask_wtf.csrf import CSRFProtect


# -----------------------------
# APPLICATION CONFIGURATION
# -----------------------------

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "temporary-development-key"
)

csrf = CSRFProtect(app)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")

if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
    raise RuntimeError(
        "Admin credentials are missing. "
        "Set ADMIN_USERNAME and ADMIN_PASSWORD_HASH."
    )


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------

def init_db():
    conn = sqlite3.connect("database.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            resolution_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = conn.execute(
        "PRAGMA table_info(tickets)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "resolution_notes" not in column_names:
        conn.execute(
            "ALTER TABLE tickets ADD COLUMN resolution_notes TEXT"
        )

    conn.commit()
    conn.close()


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# TICKET SUBMISSION
# -----------------------------

@app.route("/ticket", methods=["GET", "POST"])
def ticket():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        category = request.form["category"]
        priority = request.form["priority"]
        description = request.form["description"].strip()

        if not all([
            full_name,
            email,
            category,
            priority,
            description
        ]):
            return "Please complete all fields.", 400

        conn = sqlite3.connect("database.db")

        conn.execute("""
            INSERT INTO tickets
            (full_name, email, category, priority, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            category,
            priority,
            description
        ))

        conn.commit()
        conn.close()

        return "Your support ticket has been submitted successfully!"

    return render_template("ticket.html")


# -----------------------------
# RETRIEVE AND SEARCH TICKETS
# -----------------------------

def get_tickets(search=""):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM tickets
            WHERE full_name LIKE ?
            OR email LIKE ?
            OR description LIKE ?
            OR category LIKE ?
            OR priority LIKE ?
            ORDER BY created_at DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:
        cursor.execute("""
            SELECT * FROM tickets
            ORDER BY created_at DESC
        """)

    tickets = cursor.fetchall()

    conn.close()

    return tickets


# -----------------------------
# ADMIN LOGIN
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if (
            username == ADMIN_USERNAME
            and check_password_hash(ADMIN_PASSWORD_HASH, password)
        ):
            session.clear()
            session["logged_in"] = True

            return redirect(url_for("dashboard"))

        return "Invalid username or password.", 401

    return render_template("login.html")


# -----------------------------
# ADMIN LOGOUT
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    tickets = get_tickets(search)

    total_tickets = len(tickets)

    open_tickets = sum(
        1 for ticket in tickets if ticket[6] == "Open"
    )

    in_progress = sum(
        1 for ticket in tickets if ticket[6] == "In Progress"
    )

    resolved_tickets = sum(
        1 for ticket in tickets if ticket[6] == "Resolved"
    )

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        in_progress=in_progress,
        resolved_tickets=resolved_tickets,
        search=search
    )


# -----------------------------
# UPDATE TICKET STATUS
# -----------------------------

@app.route("/update/<int:ticket_id>", methods=["POST"])
def update_ticket(ticket_id):

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    new_status = request.form.get("status", "")

    resolution_notes = request.form.get(
        "resolution_notes", ""
    ).strip()

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        return "Invalid status.", 400

    conn = sqlite3.connect("database.db")

    conn.execute("""
        UPDATE tickets
        SET status = ?, resolution_notes = ?
        WHERE id = ?
    """, (
        new_status,
        resolution_notes,
        ticket_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -----------------------------
# START APPLICATION
# -----------------------------

init_db()

if __name__ == "__main__":
    app.run(debug=True)
