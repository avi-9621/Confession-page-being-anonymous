from flask import Flask, request, render_template, redirect, url_for
import sqlite3
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username', 'Anonymous')
        message = request.form.get('message', '')
        if message.strip():
            conn = sqlite3.connect('confessions.db')
            c = conn.cursor()
            c.execute('INSERT INTO confessions (username, message) VALUES (?, ?)', (username, message))
            conn.commit()
            conn.close()
        return redirect(url_for('home', submitted='true'))

    submitted = request.args.get('submitted') == 'true'
    return render_template('index.html', submitted=submitted)
if __name__ == '__main__':
    app.run(debug=True)
