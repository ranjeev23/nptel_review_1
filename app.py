from flask import Flask, render_template, redirect, url_for, request, session, Response
from flask import jsonify
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
            reg_no = my_db_connect.get_regno(email)
            session["regno"] = reg_no
            return redirect(url_for("student"))
        if user == "teacher":
            return redirect(url_for("yearwise_statistics"))
        else:
            return "Invalid username or password"


# Admin homepage route
# @app.route("/admin")
# def admin_homepg():
#     return render_template("admin_homepg.html")


# Student homepage route
@app.route("/student")
def student():
    std_username = session["username"]
    std_regno = session["regno"]
    std_info = my_db_connect.get_details_student(std_regno)
    verified = my_db_connect.get_verified_details(std_regno)
    nverified = my_db_connect.get_nverified_details(std_regno)
    rejected = my_db_connect.get_rej_details(std_regno)
    print("WELCOME TO STUDENT LOGIN PAGE\m")
    print("this is verified data and is in formatt\n")
    print(std_info)
    print()
    print("this is verified data and is in formatt\n")
    print(verified)
    print()
    print("this is not_verified data and is in formatt\n")
    print(nverified)
    print("this is rejected data and is in formatt\n")
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
        regno = session["regno"]
        course = request.form["course"]
        marks = request.form["marks"]

        if "certificate" not in request.files:
            return None

        certificate_file = request.files["certificate"]

        # write the code to extract the qr code here

        if certificate_file:
            file_name = email_id + course + ".pdf"
            file_name = file_name.lower().replace(" ", "_")
            certificate_file.save(os.path.join("./static/upload/", file_name))

            my_db_connect.ins_certificate(regno, course, marks, "link1", file_name)

            return render_template("success.html")


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
    print(std_marks_info)
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
@app.route("/verify_cert/<regno>/<c_code>")
def verify_cert(regno, c_code):
    file_name = my_db_connect.get_file_name(regno, c_code)
    file_name = "/upload/" + file_name
    text_details = my_db_connect.get_ver_details_admin(regno, c_code)

    print(text_details)

    return render_template(
        "cert_check.html", filename=file_name, details=text_details, c_code=c_code
    )


@app.route("/execute_function", methods=["POST"])
def correct():
    print(request.form)

    # admin_mail_id
    email_id = session["username"]

    reg_no = request.form["registerNo"]
    c_code = request.form["courseCode"]
    verified_marks = request.form["marks"]

    print((email_id, reg_no, c_code, verified_marks))
    my_db_connect.update_cert_correct(reg_no, c_code)
    my_db_connect.ins_nptel_marks(reg_no, c_code, verified_marks)
    print("succesfully added to correct db")
    return jsonify("succesfully added to correct db")


# please use this function
@app.route("/delete-certificate", methods=["POST"])
def delete_certificate():
    reg_no = request.form["reg_no"]
    c_code = request.form["c_code"]
    cert_link = my_db_connect.delete_certificate(reg_no, c_code)

    file_path = "./static/upload/" + cert_link

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted successfully.")
        return Response(200)
    else:
        print(f"{file_path} does not exist.")
        return Response(404)


@app.route("/wrong", methods=["POST"])
def wrong():
    reg_no = request.form["registerNo"]
    c_code = request.form["courseName"]
    teacher_email = session["username"]
    issue = request.form["issue"]
    my_db_connect.add_rejected(reg_no, c_code, teacher_email, issue)
    my_db_connect.update_cert_wrong(reg_no, c_code)
    print("succesfully added to wrong db")


@app.route("/admin")
def yearwise_statistics():
    print(request.method)
    if request.method == "GET":

        # real data
        acc_year = my_db_connect.getDistinctAcademicYears()
        sem_type = my_db_connect.getDistinctSemesterTypes()
        # Sample data for GET request
        yearwise_enrollment_data = my_db_connect.enorllemntcountyearwise()
        subject_enrollment_data = my_db_connect.course_enrollment_count()

        context = {
            "acc_year": acc_year,
            "sem_type": sem_type,
            "yearwise_enrollment_data": yearwise_enrollment_data,
            "subject_enrollment_data": subject_enrollment_data,
            "post_request": False,
        }
        print("********")
        print(context)
        print("rendering template")
        return render_template("yearwise_statistics.html", **context)

    elif request.method == "POST":
        print("2222222")
        course_selected = request.form["course_selected"]
        sem_selected = request.form["sem_selected"]
        print("!!!!!!")
        print(course_selected)
        print(sem_selected)

        # real data
        acc_year = my_db_connect.getDistinctAcademicYears()
        sem_type = my_db_connect.getDistinctSemesterTypes()
        enrollment_count = my_db_connect.getUniqueRegnoCountBySemTypeAndYear(
            course_selected, sem_selected
        )
        course_count = my_db_connect.getUniqueCourseCodeCountBySemTypeAndYear(
            course_selected, sem_selected
        )
        markshare_50_80 = my_db_connect.getEnrolledCountGroupedByYearAndSemType()
        sem_enrollment = my_db_connect.getSemesterWiseCountByYearAndSemType(
            course_selected, sem_selected
        )
        toppers_data = my_db_connect.getToppersgivenSemandYear(
            sem_selected, course_selected
        )
        print("ofvotr", toppers_data)
        context = {
            "selected_year": course_selected,
            "selected_sem": sem_selected,
            "acc_year": acc_year,
            "sem_type": sem_type,
            "enrollment_count": enrollment_count,
            "course_count": course_count,
            "markshare_50_80": markshare_50_80,
            "sem_enrollment": sem_enrollment,
            "toppers_data": toppers_data,
        }
        return render_template("yearwise_statistics.html", **context, post_request=True)


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8000)
