from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "secret_key")

@app.route('/', methods=['POST', 'GET'])
def index():
    bmr = None
    bmi = None

    if request.method == 'POST':
        name = request.form.get('name')
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        age = float(request.form.get('age'))
        gender = request.form.get('gender')

        if gender == 'f':
            bmr = round(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age),1)
        elif gender == 'm':
            bmr = round( 88.362 + (13.397 * weight) + (4.799 * height) - (5.667 * age),1)

        bmi = round(weight / ((height / 100) ** 2), 1)

        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS health (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        height FLOAT NOT NULL,
                        weight FLOAT NOT NULL,
                        gender TEXT NOT NULL,
                        bmr FLOAT,
                        bmi FLOAT
                     )''')
        c.execute("INSERT INTO health (name, age, height, weight, gender, bmr, bmi) VALUES (0,0,0")
        conn.commit()
        conn.close()

        return render_template('index.html', bmr=bmr, bmi=bmi)
  
    else:
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM health ORDER BY id DESC LIMIT 1")
            row = c.fetchone()
            conn.close()

            if row is not None:
                calorie = row[6]
                bmi = row[7]

            return render_template('index.html', bmr=bmr, bmi=bmi)
        except sqlite3.OperationalError:
            conn.close()
            return render_template('index.html', bmr=bmr, bmi=bmi)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
