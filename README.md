# NexHireAI 🚀

NexHireAI is a web-based job portal built using Flask, SQL Server, HTML, CSS, and JSearch API. The platform allows users to register, create profiles, search for jobs, apply for jobs, and view application history. It also integrates real-time job listings from the JSearch API.

## Features

* User Registration and Login Authentication
* User Profile Management
* Job Posting System
* Job Application Tracking
* Resume Upload Support
* Real-Time Job Search using JSearch API
* SQL Server Database Integration
* Responsive Dashboard Interface

## Technologies Used

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS

### Database

* Microsoft SQL Server

### API

* JSearch API (RapidAPI)

## Project Structure

```text
NexHireAI/
│
├── app.py
├── NexHireAI database.sql
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── add_job.html
│   ├── post_job.html
│   ├── my_applications.html
│   ├── view_applicants.html
│   └── api_users.html
│
├── static/
│   ├── dashboard.css
│   └── landing.css
│
└── uploads/
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/nikhi199/NexHireAI.git
cd NexHireAI
```

### 2. Install Dependencies

```bash
pip install flask
pip install pyodbc
pip install requests
```

### 3. Configure Database

* Open SQL Server.
* Create a database named `NexHireAI`.
* Execute the provided SQL script:

  * `NexHireAI database.sql`

### 4. Configure API Key

Replace:

```python
"x-rapidapi-key": "ADD_YOUR_RAPIDAPI_KEY_HERE"
```

with your own RapidAPI key.

### 5. Run Project

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Screenshots

Add screenshots of:

* Login Page
* Dashboard
* Job Search Results
* Profile Page
* My Applications

## Future Enhancements

* AI Resume Analyzer
* Job Recommendation System
* Email Notifications
* Resume Parsing
* Admin Dashboard
* Interview Preparation Module

## Author

**Nikhil Gole**

Aspiring Data Engineer | Python | SQL | Flask Developer

GitHub:
https://github.com/nikhi199
