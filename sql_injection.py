from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize database with some names
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL)''')

    # Insert sample users
    sample_users = [("Alice",), ("Bob",), ("Charlie",)]
    c.executemany("INSERT OR IGNORE INTO users (name) VALUES (?)", sample_users)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form["name"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # **Vulnerable Query (Direct String Concatenation)**
        query = f"SELECT * FROM users WHERE name = '{name}'"
        print("[DEBUG] Executing SQL Query:", query)  # Debugging output
        c.executescript(query)
        users = c.fetchall()  # Get all matching users instead of just one
        conn.close()

        if users:
            return f"Expected Query: {query}<br>" + "<br>".join([f"User Found: {user[1]}" for user in users])
        else:
            return f"Expected Query: {query}<br>No results found."

    return render_template_string("""
        <form method="post">
            Search for a user: <input type="text" name="name"><br>
            <input type="submit" value="Search">
        </form>
    """)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
