from flask import Flask, render_template, request, redirect, url_for, session
import os
import boto3
import uuid
from datetime import datetime, timezone

# =====================
# Flask App Setup
# =====================
app = Flask(__name__)
app.secret_key = "cloudclass_secret_key"

# =====================
# AWS DynamoDB Setup
# =====================
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1', aws_access_key_id='AKIAU5LH6CFHU5CO42Z5', aws_secret_access_key='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'
)

users_table = dynamodb.Table('Faculty-Student-Users')
courses_table = dynamodb.Table('Courses')
activities_table = dynamodb.Table('Activities')

# =====================
# AWS SNS Setup
# =====================
sns = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAU5LH6CFHU5CO42Z5', aws_secret_access_key='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'  )

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:337909780815:MyCloudClass"


def send_notification(subject, message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )

# =====================
# Routes
# =====================

@app.route('/')
def index():
    return render_template('index.html')


# ---------------------
# Register
# ---------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        users_table.put_item(
            Item={
                'email': email,
                'password': password,
                'role': role,
                'created_at': str(datetime.now(timezone.utc))
            }
        )
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------------
# Login
# ---------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        response = users_table.get_item(Key={'email': email})

        if 'Item' in response and response['Item']['password'] == password:
            session['user'] = email
            session['role'] = response['Item']['role']

            if session['role'] == 'student':
                return redirect('/student/dashboard')
            else:
                return redirect('/faculty/dashboard')

    return render_template('login.html')


# ---------------------
# Logout
# ---------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ---------------------
# Student Dashboard
# ---------------------
@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/login')

    courses = courses_table.scan().get('Items', [])
    activities = activities_table.scan().get('Items', [])

    return render_template(
        'student_dashboard.html',
        courses=courses,
        activities=activities
    )


# ---------------------
# Faculty Dashboard
# ---------------------
@app.route('/faculty/dashboard')
def faculty_dashboard():
    if session.get('role') != 'faculty':
        return redirect('/login')

    activities = activities_table.scan().get('Items', [])

    return render_template(
        'faculty_dashboard.html',
        activities=activities
    )


# ---------------------
# Upload Course Content
# ---------------------
@app.route('/upload_content', methods=['GET', 'POST'])
def upload_content():
    if session.get('role') != 'faculty':
        return redirect('/login')

    if request.method == 'POST':
        course = request.form['course']
        material = request.form['material']

        courses_table.put_item(
            Item={
                'course_name': course,
                'material': material,
                'faculty_email': session['user'],
                'created_at': str(datetime.now(timezone.utc))
            }
        )
        return redirect('/faculty/dashboard')

    return render_template('upload_content.html')


# ---------------------
# Course Detail
# ---------------------
@app.route('/course/<course_name>')
def course_detail(course_name):
    course = courses_table.get_item(
        Key={'course_name': course_name}
    ).get('Item')

    return render_template('course_detail.html', course=course)


# ---------------------
# Course Enrollment (Payment)
# ---------------------
@app.route('/payment/<course_name>')
def payment(course_name):
    email = session['user']

    activities_table.put_item(
        Item={
            'user_email': email,
            'activity_type_id': str(uuid.uuid4()),
            'activity': f'Enrolled in {course_name}',
            'course_name': course_name,
            'time': str(datetime.now(timezone.utc))
        }
    )

    send_notification(
        "Course Enrollment Successful",
        f"You have successfully enrolled in {course_name}."
    )

    return render_template('payment.html', course=course_name)


# ---------------------
# Project Submission
# ---------------------
@app.route('/submit_project/<course_name>', methods=['GET', 'POST'])
def submit_project(course_name):
    if request.method == 'POST':
        filename = request.form['filename']
        email = session['user']

        activities_table.put_item(
            Item={
                'user_email': email,
                'activity_type_id': str(uuid.uuid4()),
                'activity': f'Submitted {filename} for {course_name}',
                'course_name': course_name,
                'time': str(datetime.now(timezone.utc))
            }
        )

        send_notification(
            "Project Submitted",
            f"Your project '{filename}' for {course_name} was submitted successfully."
        )

        return redirect('/student/dashboard')

    return render_template('project_submit.html')


# ---------------------
# Quiz Submission
# ---------------------
@app.route('/quiz/<course_name>', methods=['GET', 'POST'])
def quiz(course_name):
    if request.method == 'POST':
        score = request.form['score']
        email = session['user']

        activities_table.put_item(
            Item={
                'user_email': email,
                'activity_type_id': str(uuid.uuid4()),
                'activity': f'Quiz score {score} in {course_name}',
                'course_name': course_name,
                'time': str(datetime.now(timezone.utc))
            }
        )

        send_notification(
            "Quiz Submitted",
            f"You scored {score} in the {course_name} quiz."
        )

        return redirect('/student/dashboard')

    return render_template('quiz.html')


# ---------------------
# Notifications Page (from DynamoDB)
# ---------------------
@app.route('/notifications')
def notifications():
    email = session.get('user')

    response = activities_table.query(
        KeyConditionExpression="user_email = :e",
        ExpressionAttributeValues={":e": email}
    )

    return render_template('notifications.html', data=response.get('Items', []))


# ---------------------
# Evaluate Project (Faculty)
# ---------------------
@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if session.get('role') != 'faculty':
        return redirect('/login')

    if request.method == 'POST':
        student = request.form['student']
        grade = request.form['grade']

        activities_table.put_item(
            Item={
                'user_email': student,
                'activity_type_id': str(uuid.uuid4()),
                'activity': f'Grade assigned: {grade}',
                'time': str(datetime.now(timezone.utc))
            }
        )

        send_notification(
            "Project Evaluated",
            f"Your project has been evaluated. Grade: {grade}"
        )

        return redirect('/faculty/dashboard')

    return render_template('evaluate.html')


# =====================
# Run Application
# =====================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
