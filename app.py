from flask import Flask, render_template, redirect, url_for, request, session
from database import db_class
import os

app = Flask(__name__)

# Initialize db connection
my_db_connect = db_class.mysql_connector(
    "localhost", "root", "password", "nptel_management"
)

# Set a secret key
app.secret_key = "BAD_SECRET_KEY"


# done
# Homepage route
@app.route("/")
def index():
    print("innn")
    return render_template("login.html")


# done
# Login route
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["username"]
        password = request.form["password"]

        session["username"] = email

        user = my_db_connect.validate_password(email, password)
        if user == "student":
            return redirect(url_for("student"))
        if user == "teacher":
            return redirect(url_for("admin_homepg"))
        else:
            return "Invalid username or password"


# Admin homepage route
@app.route("/admin")
def admin_homepg():
    return render_template("admin_homepg.html")


# Student homepage route
@app.route("/student")
def student():
    std_username = session["username"]
    std_info = my_db_connect.get_details_student(std_username)
    verified = my_db_connect.get_verified_details(std_username)
    nverified = my_db_connect.get_nverified_details(std_username)
    rejected = my_db_connect.get_rej_details(std_username)
    print("WELCOME TO STUDENT LOGIN PAGE")
    print()
    print("this is verified data and is in formatt")
    print()
    print(std_info)
    print()
    print("this is verified data and is in formatt")
    print()
    print(verified)
    print()
    print("this is not_verified data and is in formatt")
    print()
    print(nverified)
    print("this is rejected data and is in formatt")
    print()
    print(rejected)
    print()
    return render_template(
        "student_homepg.html",
        std_info=std_info,
        verified=verified,
        nverified=nverified,
        rejected=rejected,
    )


@app.route("/view_marksheet/<course>")
def view_marksheet(course):
    # Assuming you have some logic to fetch marksheet data based on the course
    # Replace this with your actual logic to fetch marksheet data
    marksheet_data = {
        "course": course,
        "marks": {
            "maths": 90,
            "science": 85,
            "history": 88,
            # Add more subjects and marks as needed
        },
    }
    return render_template("marksheet.html", marksheet=marksheet_data)


# Registration route
@app.route("/registration")
def registration():
    std_username = session["username"]
    available_course = my_db_connect.get_available_course(std_username)
    course_data = {
        "Database Management Systems": {
            "c_code": "IT101",
            "c_name": "Database Management Systems",
            "weeks": 12,
            "nptel_link": "https://nptel.com/it101",
            "dept": "IT",
            "acc_year": "2024-2025",
        },
        "Mechatronics": {
            "c_code": "ME501",
            "c_name": "Mechatronics",
            "weeks": 8,
            "nptel_link": "https://nptel.com/me501",
            "dept": "IT",
            "acc_year": "2021-2022",
        },
    }
    return render_template(
        "student_registration.html",
        available_course=available_course,
        course_data=course_data,
    )


# Certificate upload route
@app.route("/upload_certificate", methods=["POST"])
def upload_certificate():
    if request.method == "POST":
        email_id = session["username"]
        course = request.form["course"]
        marks = request.form["marks"]

        if "certificate" not in request.files:
            return None

        certificate_file = request.files["certificate"]

        #write the code to extract the qr code here

        if certificate_file:
            file_name = email_id + course + ".pdf"
            file_name = file_name.lower().replace(" ", "_")
            certificate_file.save(os.path.join("./static/upload/", file_name))

            my_db_connect.ins_certificate(email_id,course,marks,'link1',file_name)

            return render_template(
                "success.html",
            )


# Results page route
@app.route("/results")
def results():
    email_id = session["username"]
    available_course = my_db_connect.get_available_course(email_id)
    return render_template("marksheet_upload.html", available_course=available_course)


# this page can be removed for now
# Statistics page route
@app.route("/statistics")
def statistics():
    sorted_marks = sorted(mock_student_marks.items(), key=lambda x: x[1], reverse=True)
    return render_template("student_history.html", student_marks=sorted_marks)


# Verification page route
@app.route("/verification")
def verification():
    std_marks_info = my_db_connect.student_details()
    return render_template("admin_verification.html", std_marks_info=std_marks_info)


# Select page route
@app.route("/select")
def select():
    return render_template("course_select.html")


# Credits page route
@app.route("/credits")
def credits():
    pass


# Admin result page route
@app.route("/admin_result")
def admin_result():
    verified_details = my_db_connect.verified_details()
    return render_template("admin_viewer.html", verified_details=verified_details)


# Verify certificate page route
@app.route("/verify_cert/<email_id>/<c_code>")
def verify_cert(email_id,c_code):
    file_name = my_db_connect.get_file_name(email_id, c_code)
    file_name = '/upload/'+file_name

    text_details = my_db_connect.get_ver_details_admin(email_id, c_code)

    return render_template(
        "cert_check.html",
        filename=file_name,
        details=text_details
    )

def correct(email_id,c_code,verified_marks):
    my_db_connect.update_cert_correct(email_id,c_code)
    my_db_connect.ins_nptel_marks(email_id,c_code,verified_marks)
    print('succesfully added to correct db')

def wrong(email_id,c_code,verified_marks):
    my_db_connect.update_cert_wrong(email_id,c_code)
    print('succesfully added to wrong db')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
