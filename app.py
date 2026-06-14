from flask import Flask, render_template, request, redirect, session
import pyodbc
import requests

app = Flask(__name__)
app.secret_key = 'secret123'


# 🔗 Database Connection
def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=NIKHIL-GOLE\\SQLEXPRESS;'
        'DATABASE=NexHireAI;'
        'Trusted_Connection=yes;'
    )


# 🧑‍💻 API Users
@app.route('/api_users')
def api_users():

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users"
    )

    users = response.json()

    return render_template(
        'api_users.html',
        users=users
    )

def get_api_jobs(search_term="SQL developer Fresher jobs in india"):

    url = "https://jsearch.p.rapidapi.com/search-v2"

    querystring = {
        "query": search_term,
        "num_pages": "1",
        "country": "in",
        "date_posted": "all"
    }

    headers = {
        "x-rapidapi-key": "0992c53ce0msh12ea88e2f959e0ep15a3c5jsn431abc3adf40",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params=querystring
    )

    data = response.json()

    print("FULL API RESPONSE:")
    print(data)

    if "jobs" in data:
        return data["jobs"]

    if "data" in data and "jobs" in data["data"]:
        return data["data"]["jobs"]

    return []


# 🏠 Home Page
@app.route('/')
def home():
    return render_template('landing.html')


# 🔐 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        skills = request.form.get('skills')   # ✅ FIXED (no crash)

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
        email = request.form.get('email')
        password = request.form.get('password')

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


# 📊 Dashboard (WITH SEARCH 🔥)
@app.route('/dashboard')
def dashboard():

    print("DASHBOARD ROUTE HIT")

    search = request.args.get('search')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Jobs")
    jobs = cursor.fetchall()

    conn.close()

    api_jobs = get_api_jobs()

    print("API JOBS RETURNED:")
    print(api_jobs)

    return render_template(
        'dashboard.html',
        jobs=jobs,
        api_jobs=api_jobs
    )


# 🧑‍💼 Recruiter Info Page
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form.get('company')
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        phone = request.form.get('phone')

        return redirect('/post_job')

    return render_template('add_job.html')


# 🧾 Post Job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():

    if request.method == 'POST':

        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        skills_required = request.form['skills_required']
        salary = request.form['salary']
        description = request.form['description']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Jobs
            (
                title,
                company,
                location,
                skills_required,
                salary,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            company,
            location,
            skills_required,
            salary,
            description
        ))

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('post_job.html')

# 👤 Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'username' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':

        skills = request.form['skills']
        education = request.form['education']
        experience = request.form['experience']

        cursor.execute(
            """
            UPDATE Users
            SET skills=?,
                Education=?,
                Experience=?
            WHERE name=?
            """,
            (
                skills,
                education,
                experience,
                session['username']
            )
        )

        conn.commit()

    cursor.execute(
        "SELECT * FROM Users WHERE name=?",
        (session['username'],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        'profile.html',
        user=user
    )


# 📝 Apply for Job
@app.route('/apply/<int:job_id>')
def apply_job(job_id):

    if 'username' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM Users WHERE name=?",
        (session['username'],)
    )

    user = cursor.fetchone()

    if user:

        # Check already applied
        cursor.execute(
            """
            SELECT * FROM Applications
            WHERE user_id=? AND job_id=?
            """,
            (user.user_id, job_id)
        )

        existing = cursor.fetchone()

        if not existing:

            cursor.execute(
                """
                INSERT INTO Applications
                (user_id, job_id)
                VALUES (?, ?)
                """,
                (user.user_id, job_id)
            )

            conn.commit()

    conn.close()

    return redirect('/dashboard')

# 📂 My Applications
@app.route('/my_applications')
def my_applications():

    if 'username' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM Users WHERE name=?",
        (session['username'],)
    )

    user = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            Jobs.title,
            Jobs.company,
            Jobs.location,
            Applications.status,
            Applications.apply_date
        FROM Applications
        INNER JOIN Jobs
            ON Applications.job_id = Jobs.job_id
        WHERE Applications.user_id = ?
        """,
        (user.user_id,)
    )

    applications = cursor.fetchall()

    conn.close()

    return render_template(
        'my_applications.html',
        applications=applications
    )




# view applicants for a job (recruiter side)
@app.route('/view_applicants')
def view_applicants():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Users.name,
            Users.skills,
            Jobs.title,
            Applications.status
        FROM Applications
        INNER JOIN Users
            ON Applications.user_id = Users.user_id
        INNER JOIN Jobs
            ON Applications.job_id = Jobs.job_id
    """)

    applicants = cursor.fetchall()

    conn.close()

    return render_template(
        'view_applicants.html',
        applicants=applicants
    )

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ▶ Run App
if __name__ == '__main__':
    app.run(debug=True)