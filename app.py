from flask import Flask, render_template, request, redirect, flash
from database import get_connection
from model import evaluate
import pandas as pd
import pytesseract
import cv2
import os
import re

app = Flask(__name__)
app.secret_key = "secret123"   # ✅ REQUIRED

# -------------------------------
# TESSERACT PATH
# -------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\yuvan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# -------------------------------
# FOLDERS
# -------------------------------
UPLOAD_TEACHER = "uploads/teacher_questions"
UPLOAD_STUDENT = "uploads/student_answers"

os.makedirs(UPLOAD_TEACHER, exist_ok=True)
os.makedirs(UPLOAD_STUDENT, exist_ok=True)

# -------------------------------
# OCR FUNCTION (STRONGER)
# -------------------------------
def extract_text(path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.convertScaleAbs(gray, alpha=1.7, beta=0)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    text = pytesseract.image_to_string(thresh)

    print("\n===== OCR TEXT =====\n", text)

    return text


# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return render_template("login.html")


# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=%s AND password=%s",
        (username, password),
    )

    user = cur.fetchone()
    conn.close()

    if user:
        flash("Login Successful ✅")

        if user[0] == "teacher":
            return redirect("/teacher")
        else:
            return redirect("/student")

    flash("Invalid Login ❌")
    return redirect("/")


# -------------------------------
# REGISTER
# -------------------------------
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(username,password,role) VALUES(%s,%s,%s)",
        (username, password, role),
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------------
# TEACHER DASHBOARD
# -------------------------------
@app.route("/teacher")
def teacher():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()

    conn.close()

    return render_template("teacher_dashboard.html", questions=questions)


# -------------------------------
# UPLOAD QUESTION IMAGE (FIXED)
# -------------------------------
@app.route("/upload_question_image", methods=["POST"])
def upload_question_image():

    file = request.files["image"]

    path = os.path.join(UPLOAD_TEACHER, file.filename)
    file.save(path)

    text = extract_text(path)

    lines = text.split("\n")

    questions = []
    answers = []

    for line in lines:

        line = line.strip()

        # STRICT MATCH
        if line.endswith("?"):
            questions.append(line)

        elif line.endswith("."):
            answers.append(line)

    conn = get_connection()
    cur = conn.cursor()

    for q, a in zip(questions, answers):

        cur.execute(
            "INSERT INTO questions(question,model_answer) VALUES(%s,%s)",
            (q, a),
        )

    conn.commit()
    conn.close()

    return redirect("/teacher")


# -------------------------------
# STUDENT DASHBOARD
# -------------------------------
@app.route("/student")
def student():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()

    conn.close()

    return render_template("student_dashboard.html", questions=questions)


# -------------------------------
# STUDENT ANSWERS (STRONG FIX)
# -------------------------------
@app.route("/upload_student_answers", methods=["POST"])
def upload_student_answers():

    files = request.files.getlist("images")

    full_text = ""

    for file in files:

        path = os.path.join(UPLOAD_STUDENT, file.filename)
        file.save(path)

        text = extract_text(path)
        full_text += text + "\n"

    print("\n===== FULL STUDENT TEXT =====\n", full_text)

    lines = full_text.split("\n")

    student_answers = {}
    current_q = None

    for line in lines:

        line = line.strip()

        # 🔥 HANDLE OCR MISTAKES (l, I → 1)
        line = line.replace("l", "1").replace("I", "1")

        match = re.match(r"^(\d+)[\.\)]\s*(.*)", line)

        if match:
            current_q = int(match.group(1))
            student_answers[current_q] = match.group(2)

        elif current_q:
            student_answers[current_q] += " " + line

    print("\nDetected student answers:", student_answers)

    # -------------------------------
    # DATABASE
    # -------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()

    total_score = 0
    results = []

    for q in questions:

        qid = q[0]
        question = q[1]
        model_answer = q[2]

        student_answer = student_answers.get(qid, "")

        if student_answer.strip():

            score = evaluate(student_answer.lower(), model_answer.lower())

            total_score += score

            results.append((qid, question, student_answer, score))

            cur.execute(
                """INSERT INTO results(student,question,student_answer,score)
                   VALUES(%s,%s,%s,%s)""",
                ("student", question, student_answer, score),
            )

    conn.commit()
    conn.close()

    print("\nResults generated:", results)

    return render_template(
        "result.html",
        results=results,
        total_score=total_score,
    )


# -------------------------------
# EXPORT
# -------------------------------
@app.route("/export")
def export():

    conn = get_connection()

    df = pd.read_sql("SELECT * FROM results", conn)
    df.to_csv("marks.csv", index=False)

    conn.close()

    return "Marks exported successfully"


# -------------------------------
# LOGOUT
# -------------------------------
@app.route("/logout")
def logout():
    return redirect("/")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)