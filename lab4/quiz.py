from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('results.db')
    conn.row_factory = sqlite3.Row
    return conn


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
        cursor = conn.execute(
            'SELECT id FROM results WHERE first_name = ? AND last_name = ?',
            (first_name, last_name)
        )
        existing_record = cursor.fetchone()

        if existing_record:
            conn.execute(
                'UPDATE results SET score = ? WHERE id = ?',
                (score, existing_record['id'])
            )
            message = 'Result updated successfully'
        else:
            conn.execute(
                'INSERT INTO results (first_name, last_name, score) VALUES (?, ?, ?)',
                (first_name, last_name, score)
            )
            message = 'Result saved successfully'

        conn.commit()
        conn.close()

        return jsonify({'message': message}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
     initialize_database()
    app.run(debug=True)
