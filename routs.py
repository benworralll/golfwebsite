from flask import Flask, render_template
import sqlite3

app = Flask (__name__)

@app.route('/')
def home():
    return render_template("home.html", title = "Home Page")

@app.route("/all_courses")
def all_courses():
    conn= sqlite3.connect("golfweb.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Course")
    results = cur.fetchall()
    return render_template("all_courses.html", results = results , title = "All Courses")

@app.route("/contact")
def contact():
    return render_template ("contact.html", title= "Contact Page")

    
@app.route('/golf/<int:id>')
def golf (id):
    conn = sqlite3.connect('golfweb.db')
    cur = conn.cursor()
    cur.execute ('SELECT * FROM Course WHERE id=?', (id,))
    golf = cur.fetchone()
    print(golf)
    cur.execute('SELECT Name FROM Course WHERE id=?', (golf [2],))
    review = cur.fetchone()
    return render_template( 'golf.html', golf=golf , review=review)



if __name__ == "__main__":
    app.run(debug=True)