from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    if request.method == "POST":
        task = request.form["task"]
        db.execute("INSERT INTO todo (task) VALUES (?)", (task,))
        db.commit()
        return redirect("/")

    tasks = db.execute("SELECT * FROM todo").fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM todo WHERE id=?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
