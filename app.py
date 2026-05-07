from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    c.execute("SELECT * FROM news ORDER BY id DESC")
    news = c.fetchall()

    conn.close()

    return render_template('index.html', news=news)

@app.route('/add', methods=['GET', 'POST'])
def add_news():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        image = request.form['image']

        created_at = datetime.now().strftime("%d %B %Y")

        conn = sqlite3.connect('news.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO news(title, content, image, created_at)
            VALUES (?, ?, ?, ?)
        ''', (title, content, image, created_at))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_news.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)