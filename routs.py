from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import hashlib




app = Flask (__name__)



app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Sample users for demonstration purposes
users = [
    {'id': 1, 'username': 'user1', 'password': generate_password_hash('password1')},
    {'id': 2, 'username': 'user2', 'password': generate_password_hash('password2')}
]

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/profile')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            # Authentication successful, store user ID in session
            session['user_id'] = user['id']
            return redirect('/profile')
        else:
            error = 'Invalid username or password.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        # Find user by ID
        user = next((user for user in users if user['id'] == session['user_id']), None)
        return render_template('profile.html', username=user['username'])
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run()



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