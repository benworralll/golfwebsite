from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config.from_object("config")


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/course_added")
def courses_added():
    return render_template("course_added.html", title="Course Added")


@app.route('/courses')
def courses():
    courses = [...]
    add_course_route = '/course/add'
    return render_template('courses.html', courses=courses, add_course_route=add_course_route)


@app.route('/course/add', methods=['POST'])
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
    return redirect("http://127.0.0.1:5000/course_added")


@app.route("/all_courses")
def all_courses():
    conn = sqlite3.connect("golfweb.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Courses")
    results = cur.fetchall()
    return render_template("all_courses.html", results=results, title="All Courses")


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Page")

    
@app.route('/golf/<int:id>')
def golf(id):
    conn = sqlite3.connect('golfweb.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Courses WHERE id=?', (id,))
    golf = cur.fetchone()
    print(golf)
    cur.execute('SELECT Name FROM Courses WHERE id=?', (golf[2],))
    review = cur.fetchone()
    return render_template('golf.html', golf=golf, review=review)


@app.route('/course/<int:course_id>/reviews')
def course_reviews(course_id):
    # Connect to the database
    db = sqlite3.connect('golfweb.db')
    cursor = db.cursor()

    # Retrieve the reviews for the given course_id
    cursor.execute('SELECT * FROM reviews WHERE course_id = ?', (course_id,))
    reviews = cursor.fetchall()
    return render_template('reviews.html', reviews=reviews)


@app.route('/course/<int:course_id>/reviews', methods=['POST'])
def submit_review(course_id):
    # Get the submitted review details from the request form
    rating = request.form['rating']
    comment = request.form['comment']

    # Connect to the database
    db = sqlite3.connect('golfweb.db')
    cursor = db.cursor()

    # Insert the new review into the database
    cursor.execute(
        'INSERT INTO reviews (course_id, user_id, rating, comment) VALUES (?, ?, ?, ?)',
        (course_id, g.user['id'], rating, comment)
    )
    db.commit()

    return redirect(f'/course/{course_id}/reviews')



if __name__ == "__main__":
    app.run(debug=True)