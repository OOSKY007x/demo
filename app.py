from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("it_academy.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # 1. Categories
    conn.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    # 2. Users
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, role TEXT)")
    # 3. Instructors
    conn.execute("CREATE TABLE IF NOT EXISTS instructors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, bio TEXT)")
    # 4. Courses
    conn.execute("""CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        description TEXT, 
        price REAL, 
        image TEXT, 
        category_id INTEGER,
        instructor_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id),
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    )""")
    # 5. Lessons
    conn.execute("CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER, title TEXT, content TEXT)")
    # 6. Enrollments
    conn.execute("CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER)")
    # 7. Reviews
    conn.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER, rating INTEGER, comment TEXT)")
    
    # ข้อมูลตัวอย่าง
    conn.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Web Development')")
    conn.execute("INSERT OR IGNORE INTO instructors (id, name, bio) VALUES (1, 'Ajarn Pixel', 'Expert in 8-bit Arts')")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()
    courses = conn.execute("""
        SELECT courses.*, categories.name as cat_name 
        FROM courses 
        LEFT JOIN categories ON courses.category_id = categories.id
    """).fetchall()
    conn.close()
    return render_template("index.html", courses=courses)

@app.route("/add", methods=["GET", "POST"])
def add_course():
    conn = get_db()
    if request.method == "POST":
        conn.execute("INSERT INTO courses (title, description, price, image, category_id, instructor_id) VALUES (?, ?, ?, ?, ?, ?)",
                     (request.form['title'], request.form['desc'], request.form['price'], request.form['image'], 1, 1))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)