from flask_app import Flask, request, render_template
from password_manager import PasswordManager
app = Flask("password_manager")


@app.route("/", methods=["POST", "GET"])
@app.route("/generate_password",  methods=["POST", "GET"])
def home():
    if request.method == "POST":
        password_length = int(request.form["password_length"])
        is_lower_included = request.form.get("is_lower_included") == "on"
        is_number_included = request.form.get("is_number_included") == "on"
        is_upper_included = request.form.get("is_upper_included") == "on"
        is_symbol_included = request.form.get("is_symbol_included") == "on"
        password = PasswordManager.generate_password(
            length=password_length,
            is_lower_included=is_lower_included,
            is_number_included=is_number_included,
            is_upper_included=is_upper_included,
            is_symbol_included=is_symbol_included,
        )
    else:
        password = None
    return render_template("generate_password.html", password=password)
    

app.run()