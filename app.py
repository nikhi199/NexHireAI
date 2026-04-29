from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'secret123'   # required for session


# 🔗 Database Connection
def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=NIKHIL-GOLE\\SQLEXPRESS;'
        'DATABASE=NexHireAI;'
        'Trusted_Connection=yes;'
    )


# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 🔐 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        skills = request.form['skills']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Users (name, email, password, skills) VALUES (?, ?, ?, ?)",
            (name, email, password, skills)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user.name
            return redirect('/dashboard')
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')


# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Jobs")
    job_count = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM Jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        username=session.get('username'),
        job_count=job_count,
        jobs=jobs
    )


# 🧑‍💼 Recruiter Info Page
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        first = request.form['first_name']
        last = request.form['last_name']
        phone = request.form['phone']

        return redirect('/post_job')

    return render_template('add_job.html')


# 🧾 Post Job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        skills = request.form['skills']
        salary = request.form['salary']
        description = request.form['description']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Jobs (title, location, skills_required, salary, description) VALUES (?, ?, ?, ?, ?)",
            (title, location, skills, salary, description)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('post_job.html')


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ▶ Run App
if __name__ == '__main__':
    app.run(debug=True)