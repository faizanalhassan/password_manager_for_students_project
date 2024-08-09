from flask import Flask, render_template, request
from password_manager import PasswordManager
flask_app = Flask("Password Manager")
pm = PasswordManager()
@flask_app.route("/", methods=["GET", "POST"])
@flask_app.route("/generate_password", methods=["GET", "POST"])
def generate_password():
    if request.method == "POST":
        password_length = int(request.form.get("password_length", 10))
        if request.form.get("is_lower_included") == "on":
            is_lower_included =  True
        else:
            is_lower_included = False
        if request.form.get("is_number_included") == "on":
            is_number_included = True
        else:
            is_number_included = False
        if request.form.get("is_upper_included") == "on":
            is_upper_included = True
        else:
            is_upper_included = False
        if request.form.get("is_symbol_included") == "on":
            is_symbol_included = True
        else:
            is_symbol_included = False    
        password = pm.generate_password(
            length=password_length,
            is_lower_included=is_lower_included,
            is_number_included=is_number_included,
            is_upper_included=is_upper_included,
            is_symbol_included=is_symbol_included,
        )
    else:
        password = None
        
    return render_template("genrate_password.html", password=password)


@flask_app.route("/add_credential", methods=["GET", "POST"])
def add_credential():
    messages = []
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            messages.append("Name is required")
        username = request.form.get("username")
        if not username:
            messages.append("Username is required <br>")
        password = request.form.get("password")
        if not password:
            messages.append("Password is required <br>")
        
        category = request.form.get("category")
        notes = request.form.get("notes")
        
        
    return render_template("save_credential_item.html", messages=messages)

flask_app.run(debug=True)