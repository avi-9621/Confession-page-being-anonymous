from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # <-- Replace with a secure key in production

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
        message = request.form.get('message', '').strip()
        if message:
            conn = sqlite3.connect('confessions.db')
            c = conn.cursor()
            c.execute('INSERT INTO confessions (username, message) VALUES (?, ?)', (username, message))
            conn.commit()
            conn.close()
            flash('Thank you for submitting your confession!')
        return redirect(url_for('home'))

    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
