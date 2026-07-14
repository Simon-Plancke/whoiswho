from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)
app.secret_key = "whoiswho-dev-secret"

DEFAULT_USER = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada.lovelace@whoiswho.dev",
    "address": "10 Downing Street, London",
    "hobbies": "Reading, Hiking, Tech",
    "role": "Product Designer",
    "avatar": "AL",
}

EMPLOYEES = [
    {"name": "Ada Lovelace", "role": "Product Designer", "department": "Design"},
    {"name": "Grace Hopper", "role": "Engineering Lead", "department": "Engineering"},
    {"name": "Katherine Johnson", "role": "Data Scientist", "department": "Research"},
    {"name": "Margaret Hamilton", "role": "Software Architect", "department": "Product"},
]


def get_user():
    return session.get("user", DEFAULT_USER)


@app.get("/")
def index():
    if session.get("authenticated"):
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.get("/login")
@app.post("/login")
def login():
    if request.method == "POST":
        session["authenticated"] = True
        session["user"] = {
            **DEFAULT_USER,
            "first_name": request.form.get("first_name", DEFAULT_USER["first_name"]),
            "last_name": request.form.get("last_name", DEFAULT_USER["last_name"]),
            "email": request.form.get("email", DEFAULT_USER["email"]),
        }
        flash("Signed in successfully through SSO", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.get("/home")
def home():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template("home.html", user=get_user(), employees=EMPLOYEES)


@app.post("/home")
def update_profile():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    current_user = get_user()
    updated_user = {
        **current_user,
        "first_name": request.form.get("first_name", current_user["first_name"]),
        "last_name": request.form.get("last_name", current_user["last_name"]),
        "address": request.form.get("address", current_user.get("address", "")),
        "hobbies": request.form.get("hobbies", current_user.get("hobbies", "")),
        "email": request.form.get("email", current_user["email"]),
        "avatar": f"{request.form.get('first_name', current_user['first_name'])[0].upper()}{request.form.get('last_name', current_user['last_name'])[0].upper()}",
    }
    session["user"] = updated_user
    flash("Your profile information was updated", "success")
    return redirect(url_for("home"))


@app.get("/employees")
def employees():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template("employees.html", employees=EMPLOYEES, user=get_user())


@app.get("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
