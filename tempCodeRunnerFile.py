from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mahesh123",  # your MySQL password
    database="gym_db"
)
cursor = db.cursor(dictionary=True)

# Membership Plans
plans = {
    "1 Month": 1000,
    "3 Months": 2500,
    "6 Months": 4500,
    "1 Year": 8000
}
trainer_extra = {
    "1 Month": 1500,
    "3 Months": 4000,
    "6 Months": 7000,
    "1 Year": 12000
}

def calculate_end_date(start_date, plan):
    days = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365}
    return start_date + timedelta(days=days[plan])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        age = data['age']
        weight = data['weight']
        height = data['height']
        reason = data['reason']
        plan = data['plan']
        trainer_req = 'trainer_required' in data
        trainer_id = data.get('trainer_id')
        total = plans[plan] + (trainer_extra[plan] if trainer_req else 0)
        start_date = date.today()
        end_date = calculate_end_date(start_date, plan)

        sql = """INSERT INTO members 
                 (name, age, weight, height, reason, membership_plan, trainer_required, trainer_id, start_date, end_date, total_amount)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (name, age, weight, height, reason, plan, trainer_req, trainer_id, start_date, end_date, total)
        cursor.execute(sql, val)
        db.commit()
        return redirect('/view_members')

    cursor.execute("SELECT * FROM trainers")
    trainers = cursor.fetchall()
    return render_template('add_member.html', plans=plans, trainers=trainers)

@app.route('/view_members')
def view_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    return render_template('view_members.html', members=members)

@app.route('/cancel/<int:member_id>')
def cancel(member_id):
    cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
    db.commit()
    return redirect('/view_members')

@app.route('/view_trainers')
def view_trainers():
    cursor.execute("SELECT * FROM trainers")
    trainers = cursor.fetchall()
    return render_template('view_trainers.html', trainers=trainers)

if __name__ == '__main__':
    app.run(debug=True)
