from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash
import sqlite3
import hashlib




app = Flask (__name__)

app.secret_key = 'test'

@app.route('/')
def home():
    return render_template("home.html", title = "Home Page")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        db = sqlite3.connect('golfweb.db')
        cursor = db.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()

        # Redirect to a success page or login page
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        db = sqlite3.connect('golfweb.db')
        cursor = db.cursor()

        # Retrieve the user's stored password hash based on the username
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user is None:
            error = 'Invalid username or password.'
            return render_template('login.html', error=error)

        stored_password_hash = user[0]

        # Compare the provided password with the stored password hash
        if check_password_hash(stored_password_hash, password):
            # Authentication successful
            # Perform any necessary actions (e.g., redirect to the user's profile page)
            return redirect('/profile')

        error = 'Invalid username or password.'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/course_added', methods=['POST'])
def add_course():
    name = request.form['name']
    location = request.form['location']
    description = request.form['description']
    par = int(request.form['par'])
    yardage = int(request.form['yardage'])
    rating = float(request.form['rating'])
    slope = int(request.form['slope'])


    conn = sqlite3.connect('golfweb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Courses (name, location, description, par, yardage, rating, slope) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (name, location, description, par, yardage, rating, slope))
    conn.commit()


    return ("Succesfully added your course!!")

@app.route('/courses')
def courses():

    courses = [...]
    
    add_course_route = '/course/add'

    return render_template('courses.html', courses=courses, add_course_route=add_course_route)



@app.route("/all_courses")
def all_courses():
    conn= sqlite3.connect("golfweb.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses")
    results = cur.fetchall()
    return render_template("all_courses.html", results = results , title = "All Courses")

@app.route("/contact")
def contact():
    return render_template ("contact.html", title= "Contact Page")

    
@app.route('/golf/<int:id>')
def golf (id):
    conn = sqlite3.connect('golfweb.db')
    cur = conn.cursor()
    cur.execute ('SELECT * FROM Courses WHERE id=?', (id,))
    golf = cur.fetchone()
    print(golf)
    cur.execute('SELECT Name FROM Courses WHERE id=?', (golf [2],))
    review = cur.fetchone()
    return render_template( 'golf.html', golf=golf , review=review)



if __name__ == "__main__":
    app.run(debug=True)