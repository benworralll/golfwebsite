from flask import Flask, render_template, request
import sqlite3

app = Flask (__name__)

@app.route('/')
def home():
    return render_template("home.html", title = "Home Page")

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


    return render_template('courses_added.html')

@app.route('/courses')
def courses():

    courses = [...]
    
    add_course_route = '/course_added'

    return render_template('courses.html', courses=courses, add_course_route=add_course_route)


@app.route("/course_added")
def course_added():
    return render_template ("course_added.html", title= "course added")

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

    
@app.route('/golf/<int:course_id>')
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