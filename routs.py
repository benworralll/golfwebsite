from flask import Flask, render_template, request
import sqlite3

app = Flask (__name__)

@app.route('/')
def home():
    return render_template("home.html", title = "Home Page")

@app.route('/courses/add', methods=['POST'])
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
    conn.commit


    return 'Course added successfully!'

@app.route('/courses')
def courses():
    # Assuming you have a list of courses to display
    courses = [...]
    
    # Assuming you have a route for adding courses
    add_course_route = '/courses/add'

    return render_template('courses.html', courses=courses, add_course_route=add_course_route)


# @app.route('/courses')
# def courses():
  #  conn = sqlite3.connect('golfweb.db')
   # cursor = conn.cursor()
    #cursor.execute('SELECT * FROM Courses')
    #courses = cursor.fetchall()

    # Process the courses data and display it on your website
    # For example, you can pass the data to a template for rendering

    return render_template('courses.html', courses=courses)




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