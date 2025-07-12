import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from extensions import db
from models import Package
from forms import PackageForm
from sms import send_sms  # ✅ Infobip integration

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = PackageForm()
    if form.validate_on_submit():
        tracking_id = str(uuid.uuid4()).split("-")[0]
        new_package = Package(
            tracking_id=tracking_id,
            sender_name=form.sender_name.data,
            receiver_name=form.receiver_name.data,
            phone_sender=form.phone_sender.data,
            phone_receiver=form.phone_receiver.data
        )
        db.session.add(new_package)
        db.session.commit()
        flash(f"Package Registered! Tracking ID: {tracking_id}", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/packages")
def view_packages():
    packages = Package.query.order_by(Package.created_at.desc()).all()
    return render_template("packages.html", packages=packages)

@app.route("/update_status/<int:package_id>", methods=["POST"])
def update_status(package_id):
    new_status = request.form.get("status")
    package = Package.query.get_or_404(package_id)

    if package.status != new_status:
        package.status = new_status
        db.session.commit()

        # Build the SMS message
        message = f"Your package (ID: {package.tracking_id}) status updated to: '{new_status}'. - Cargo Express"

        # Send to both sender and receiver
        send_sms(package.phone_sender, message)
        send_sms(package.phone_receiver, message)

        flash(f"Status for package {package.tracking_id} updated and SMS sent.", "info")
    else:
        flash(f"No change for package {package.tracking_id}.", "warning")

    return redirect(url_for("view_packages"))

# ---------------------------------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)