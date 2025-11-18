from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = 'secret123'  

# ---------------- DATABASE CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="Sathish@2007",       
    database="ediary"
)
cursor = conn.cursor(dictionary=True)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('view_entries'))
        else:
            return "<script>alert('Invalid username or password'); window.location='/login';</script>"

    return render_template('login.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing = cursor.fetchone()
        if existing:
            return "<script>alert('Username already exists!'); window.location='/register';</script>"

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return "<script>alert('Registration successful! Please login.'); window.location='/login';</script>"

    return render_template('register.html')


# ---------------- VIEW ENTRIES ----------------
@app.route('/view')
def view_entries():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM entries WHERE user_id=%s ORDER BY entry_id DESC", (session['user_id'],))
    entries = cursor.fetchall()
    return render_template('view_entries.html', entries=entries)


# ---------------- ADD ENTRY ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry_date = date.today()

        cursor.execute(
            "INSERT INTO entries (user_id, title, content, entry_date) VALUES (%s, %s, %s, %s)",
            (session['user_id'], title, content, entry_date)
        )
        conn.commit()
        return redirect(url_for('view_entries'))

    return render_template('add_entry.html')


# ---------------- EDIT ENTRY ----------------
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM entries WHERE entry_id=%s AND user_id=%s", (entry_id, session['user_id']))
    entry = cursor.fetchone()

    if not entry:
        return redirect(url_for('view_entries'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE entries SET title=%s, content=%s WHERE entry_id=%s", (title, content, entry_id))
        conn.commit()
        return redirect(url_for('view_entries'))

    return render_template('edit_entry.html', entry=entry)


# ---------------- DELETE ENTRY ----------------
@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM entries WHERE entry_id=%s AND user_id=%s", (entry_id, session['user_id']))
    conn.commit()
    return redirect(url_for('view_entries'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(debug=True)
