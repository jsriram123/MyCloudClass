# CloudClass – Cloud-Based Education Platform

CloudClass is a cloud-native education management platform designed to streamline academic workflows for **students and faculty**. It provides a centralized system for course management, project submissions, quizzes, evaluations, and real-time notifications using AWS services.

---

## 📌 Project Overview

Traditional academic workflows often rely on emails and manual tracking, leading to confusion, delays, and lack of transparency. CloudClass solves this problem by providing a **role-based, cloud-hosted platform** where students and faculty can interact efficiently.

The application is built using **Flask** for backend logic, **AWS DynamoDB** for data storage, **AWS SNS** for notifications, and is hosted on **AWS EC2**.

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python Flask

### Cloud & AWS Services
- AWS EC2 – Application hosting
- AWS DynamoDB – NoSQL database
- AWS SNS – Email notifications
- AWS IAM – Role-based access control

---

## 📂 Project Structure

```
MyCloudClass/
│
├── app.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── faculty_dashboard.html
│   ├── course_detail.html
│   ├── upload_content.html
│   ├── project_submit.html
│   ├── quiz.html
│   ├── evaluate.html
│   ├── payment.html
│   └── notifications.html
│
└── utils/
```

---

## 🗄️ DynamoDB Tables

### 1. Faculty-Student-Users
- **Partition Key:** email (String)
- Stores user credentials and roles (student / faculty)

### 2. Courses
- **Partition Key:** course_name (String)
- Stores course details and study materials

### 3. Activities
- **Partition Key:** user_email (String)
- **Sort Key:** activity_type_id (String)
- Stores enrollments, submissions, quiz results, grades, and notifications

---

## 🔑 Key Features

### Student Features
- User registration and login
- View available courses
- Enroll in courses
- Submit projects
- Attempt quizzes
- Receive real-time notifications
- View activity history

### Faculty Features
- Login with role-based access
- Upload course materials
- View student submissions
- Evaluate projects and assign grades
- Trigger notifications to students

---

## 🔔 Notifications (AWS SNS)

CloudClass uses **AWS SNS** to send real-time email notifications for:
- Course enrollment confirmation
- Project submission acknowledgment
- Quiz submission results
- Project evaluation and grading updates

SNS is integrated alongside DynamoDB, where DynamoDB maintains activity history and SNS handles instant communication.

---

## 🚀 Deployment Steps (EC2)

1. Launch an EC2 instance (Amazon Linux)
2. Attach an IAM Role with:
   - AmazonDynamoDBFullAccess
   - AmazonSNSFullAccess
3. Install dependencies:
   ```bash
   sudo yum update -y
   sudo yum install python3 -y
   pip3 install flask boto3
   ```
4. Clone or upload the project files
5. Run the application:
   ```bash
   python3 app.py
   ```
6. Open inbound rule for port **5000**
7. Access the app using:
   ```
   http://<EC2-Public-IP>:5000
   ```

---

## 🧪 Running Locally

1. Install Python 3.9+
2. Install dependencies:
   ```bash
   pip install flask boto3
   ```
3. Configure AWS credentials using:
   ```bash
   aws configure
   ```
4. Run:
   ```bash
   python app.py
   ```

---

## 🎓 Academic Use Case

This project is suitable for:
- Cloud Computing projects
- AWS mini / major projects
- College final-year projects
- Demonstrating cloud-native architecture and IAM best practices

---

## 📌 Future Enhancements

- File uploads to AWS S3
- Role-based fine-grained permissions
- SMS notifications using SNS
- Analytics dashboard with charts
- Deployment using Nginx and Gunicorn

---

## 📄 License

This project is intended for **educational and academic use**.

---

## ✨ Author

Developed as part of a cloud-based academic project using AWS and Flask.

