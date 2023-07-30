from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config.from_object("config")
app.config['DATABASE'] = 'golfweb.db'


# Home page route
@app.route('/')
def home():
    return render_template('home.html')


# Route for displaying a "Course Added" message
@app.route("/course_added")
def courses_added():
    return render_template("course_added.html", title="Course Added")


# Route for displaying the "Reviews" page
@app.route("/reviews")
def reviews():
    return render_template("reviews.html", title="Reviews")


# Route for displaying all reviews from the database
@app.route('/')
def reviews_page():
    # Retrieve reviews from the database
    conn = sqlite3.connect('golfweb.db')  # Connecting to tdatabase
    cur = conn.cursor()
    cur.execute('SELECT * FROM reviews')  # Executed an SQL Query to retreave data from reviews table
    reviews = cur.fetchall()

    return render_template('reviews.html', reviews=reviews)


# Route for submitting a review for a golf course
@app.route('/submit_review', methods=['POST'])
def submit_review():
    # Retrieve review details from the form
    course_id = int(request.form['course_id'])
    username = request.form.get('username', False)
    rating = int(request.form['rating'])
    review = request.form['review']

    # Store the review in the database
    conn = sqlite3.connect('golfweb.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO reviews (course_id, username, rating, comment) VALUES (?, ?, ?, ?)',
                   (course_id, username, rating, review))
    conn.commit()

    return render_template('thank_you.html')


# Route for displaying a list of golf courses
@app.route('/courses')
def courses():
    courses = [...] # Placeholder for the list of courses
    add_course_route = '/course/add'
    return render_template('courses.html', courses=courses, add_course_route=add_course_route)


# Route for adding a new golf course
@app.route('/course/add', methods=['POST'])
def add_course():
    # Retrieve course details from the form
    name = request.form['name']
    location = request.form['location']
    description = request.form['description']
    par = int(request.form['par'])
    yardage = int(request.form['yardage'])
    rating = float(request.form['rating'])
    slope = int(request.form['slope'])

    # Store the new course in the database
    conn = sqlite3.connect('golfweb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Courses (name, location, description, par, yardage, rating, slope) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (name, location, description, par, yardage, rating, slope))
    conn.commit()
    return redirect("http://127.0.0.1:5000/course_added")


# Route for displaying all courses in the database
@app.route("/all_courses")
def all_courses():
    conn = sqlite3.connect("golfweb.db")  # Connection to the database
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses")  # Executed an SQL query to retrieve data from Courses table
    results = cur.fetchall()
    return render_template("all_courses.html", results=results, title="All Courses")


# Route for displaying the "Contact" page
@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Page")


# Route for displaying detailed information about a specific golf course
@app.route('/golf/<int:id>')
def golf(id):
    conn = sqlite3.connect('golfweb.db')  # Connection to the database
    cur = conn.cursor()
    cur.execute('SELECT * FROM Courses WHERE id=?', (id,))  # Executed a SQL query to retrieve data from the courses table for the specified id
    golf = cur.fetchone()
    print(golf)
    cur.execute('SELECT * FROM reviews WHERE course_id=?', (id,))  # Executed a SQL query to retrieve data from reviews table for the spesific course id
    reviews = cur.fetchall()

    return render_template('golf.html', golf=golf, reviews=reviews) 


if __name__ == "__main__":
    app.run(debug=True)
