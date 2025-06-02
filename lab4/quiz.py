from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Підключення до бази даних
def get_db_connection():
    conn = sqlite3.connect('results.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ініціалізація бази даних
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Головна сторінка
@app.route('/')
def index():
    return render_template('start_page.html')

# Сторінка тесту
@app.route('/quiz')
def quiz():
    return render_template('quiz_page.html')


@app.route('/api/save-result', methods=['POST'])
def save_result():
    try:
        data = request.get_json()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        score = data.get('score')

        if not all([first_name, last_name, score is not None]):
            return jsonify({'error': 'Incomplete data'}), 400

        conn = get_db_connection()
        cursor = conn.execute('INSERT INTO results (first_name, last_name, score) VALUES (?, ?, ?)', 
                               (first_name, last_name, score))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Result saved successfully', 'id': record_id}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)