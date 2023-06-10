from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/knowlege_base_command.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        command = request.form['command']
        cursor = conn.execute('SELECT * FROM KNOWLEDGE_DB WHERE command LIKE ?', (f'%{command}%',))
    else:
        cursor = conn.execute('SELECT * FROM KNOWLEDGE_DB')
    
    rows = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=rows)

if __name__ == '__main__':
    app.run(debug=True)
