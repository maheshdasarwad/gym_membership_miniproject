from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from datetime import date, timedelta, datetime
import hashlib
import secrets
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mahesh123", 
        database="gym_db"
    )

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper functions
def calculate_end_date(start_date, plan_days):
    return start_date + timedelta(days=plan_days)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_membership_plans():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM membership_plans WHERE is_active = TRUE")
    plans = cursor.fetchall()
    cursor.close()
    db.close()
    return plans

def get_trainers():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trainers WHERE is_active = TRUE")
    trainers = cursor.fetchall()
    cursor.close()
    db.close()
    return trainers

# Main Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s AND is_active = TRUE", (username,))
        admin = cursor.fetchone()
        cursor.close()
        db.close()
        
        if admin and admin['password_hash'] == hash_password(password):
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['full_name']
            session['admin_role'] = admin['role']
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Get dashboard statistics
    cursor.execute("SELECT COUNT(*) as total_members FROM members WHERE status = 'active'")
    total_members = cursor.fetchone()['total_members']
    
    cursor.execute("SELECT COUNT(*) as total_trainers FROM trainers WHERE is_active = TRUE")
    total_trainers = cursor.fetchone()['total_trainers']
    
    cursor.execute("SELECT COUNT(*) as today_attendance FROM attendance WHERE DATE(check_in_time) = CURDATE()")
    today_attendance = cursor.fetchone()['today_attendance']
    
    cursor.execute("SELECT SUM(amount) as monthly_revenue FROM payments WHERE payment_status = 'completed' AND MONTH(payment_date) = MONTH(CURDATE())")
    monthly_revenue = cursor.fetchone()['monthly_revenue'] or 0
    
    # Get recent members
    cursor.execute("SELECT * FROM members ORDER BY created_at DESC LIMIT 5")
    recent_members = cursor.fetchall()
    
    # Get upcoming class schedules
    cursor.execute("""
        SELECT cs.*, c.class_name, t.name as trainer_name 
        FROM class_schedules cs 
        JOIN classes c ON cs.class_id = c.class_id 
        LEFT JOIN trainers t ON c.trainer_id = t.trainer_id 
        WHERE cs.schedule_date >= CURDATE() AND cs.is_cancelled = FALSE 
        ORDER BY cs.schedule_date, cs.start_time 
        LIMIT 5
    """)
    upcoming_classes = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('admin_dashboard.html', 
                         total_members=total_members,
                         total_trainers=total_trainers,
                         today_attendance=today_attendance,
                         monthly_revenue=monthly_revenue,
                         recent_members=recent_members,
                         upcoming_classes=upcoming_classes)

@app.route('/admin/members')
@login_required
def admin_members():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, t.name as trainer_name 
        FROM members m 
        LEFT JOIN trainers t ON m.trainer_id = t.trainer_id 
        ORDER BY m.created_at DESC
    """)
    members = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('admin_members.html', members=members)

@app.route('/admin/add_member', methods=['GET', 'POST'])
@login_required
def admin_add_member():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data.get('email')
        phone = data.get('phone')
        age = int(data['age'])
        weight = float(data['weight'])
        height = float(data['height'])
        reason = data['reason']
        plan_id = int(data['plan_id'])
        trainer_req = data.get('trainer_required') == 'yes'
        trainer_id = int(data['trainer_id']) if data.get('trainer_id') else None
        emergency_contact = data.get('emergency_contact')
        emergency_phone = data.get('emergency_phone')
        address = data.get('address')
        
        # Get plan details
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membership_plans WHERE plan_id = %s", (plan_id,))
        plan = cursor.fetchone()
        
        if not plan:
            flash('Invalid membership plan selected!', 'error')
            return redirect(url_for('admin_add_member'))
        
        # Calculate total amount
        total_amount = plan['price']
        if trainer_req and trainer_id:
            total_amount += plan['trainer_price']
        
        start_date = date.today()
        end_date = calculate_end_date(start_date, plan['duration_days'])
        
        # Insert member
        sql = """INSERT INTO members 
                 (name, email, phone, age, weight, height, reason, membership_plan, trainer_required, trainer_id, 
                  start_date, end_date, total_amount, emergency_contact, emergency_phone, address)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (name, email, phone, age, weight, height, reason, plan['plan_name'], trainer_req, trainer_id,
               start_date, end_date, total_amount, emergency_contact, emergency_phone, address)
        cursor.execute(sql, val)
        member_id = cursor.lastrowid
        
        # Create payment record
        payment_sql = """INSERT INTO payments 
                        (member_id, amount, payment_type, payment_method, payment_status, payment_date, created_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        payment_val = (member_id, total_amount, 'membership', 'cash', 'completed', datetime.now(), session['admin_id'])
        cursor.execute(payment_sql, payment_val)
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f'Member {name} added successfully!', 'success')
        return redirect(url_for('admin_members'))
    
    plans = get_membership_plans()
    trainers = get_trainers()
    return render_template('admin_add_member.html', plans=plans, trainers=trainers)

@app.route('/admin/attendance')
@login_required
def admin_attendance():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Get today's attendance
    cursor.execute("""
        SELECT a.*, m.name as member_name, m.membership_plan
        FROM attendance a
        JOIN members m ON a.member_id = m.member_id
        WHERE DATE(a.check_in_time) = CURDATE()
        ORDER BY a.check_in_time DESC
    """)
    today_attendance = cursor.fetchall()
    
    # Get attendance statistics
    cursor.execute("SELECT COUNT(*) as total_checkins FROM attendance WHERE DATE(check_in_time) = CURDATE()")
    total_checkins = cursor.fetchone()['total_checkins']
    
    cursor.execute("SELECT COUNT(DISTINCT member_id) as unique_members FROM attendance WHERE DATE(check_in_time) = CURDATE()")
    unique_members = cursor.fetchone()['unique_members']
    
    cursor.close()
    db.close()
    
    return render_template('admin_attendance.html', 
                         today_attendance=today_attendance,
                         total_checkins=total_checkins,
                         unique_members=unique_members)

@app.route('/admin/checkin', methods=['POST'])
@login_required
def admin_checkin():
    member_id = request.form.get('member_id')
    
    if not member_id:
        return jsonify({'success': False, 'message': 'Member ID is required'})
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Check if member exists and is active
    cursor.execute("SELECT * FROM members WHERE member_id = %s AND status = 'active'", (member_id,))
    member = cursor.fetchone()
    
    if not member:
        cursor.close()
        db.close()
        return jsonify({'success': False, 'message': 'Member not found or inactive'})
    
    # Check if already checked in today
    cursor.execute("""
        SELECT * FROM attendance 
        WHERE member_id = %s AND DATE(check_in_time) = CURDATE() AND check_out_time IS NULL
    """, (member_id,))
    existing_checkin = cursor.fetchone()
    
    if existing_checkin:
        cursor.close()
        db.close()
        return jsonify({'success': False, 'message': 'Member already checked in today'})
    
    # Create check-in record
    cursor.execute("INSERT INTO attendance (member_id) VALUES (%s)", (member_id,))
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({'success': True, 'message': f'Welcome {member["name"]}! Check-in successful.'})

@app.route('/admin/checkout', methods=['POST'])
@login_required
def admin_checkout():
    member_id = request.form.get('member_id')
    
    if not member_id:
        return jsonify({'success': False, 'message': 'Member ID is required'})
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Find today's check-in record
    cursor.execute("""
        SELECT * FROM attendance 
        WHERE member_id = %s AND DATE(check_in_time) = CURDATE() AND check_out_time IS NULL
        ORDER BY check_in_time DESC LIMIT 1
    """, (member_id,))
    checkin_record = cursor.fetchone()
    
    if not checkin_record:
        cursor.close()
        db.close()
        return jsonify({'success': False, 'message': 'No active check-in found for this member'})
    
    # Calculate duration
    checkin_time = checkin_record['check_in_time']
    checkout_time = datetime.now()
    duration = int((checkout_time - checkin_time).total_seconds() / 60)
    
    # Update check-out
    cursor.execute("""
        UPDATE attendance 
        SET check_out_time = %s, duration_minutes = %s 
        WHERE attendance_id = %s
    """, (checkout_time, duration, checkin_record['attendance_id']))
    
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({'success': True, 'message': f'Check-out successful. Duration: {duration} minutes'})

# Legacy routes for backward compatibility
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    return redirect(url_for('admin_add_member'))

@app.route('/view_members')
def view_members():
    return redirect(url_for('admin_members'))

@app.route('/cancel/<int:member_id>')
def cancel(member_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE members SET status = 'cancelled' WHERE member_id = %s", (member_id,))
    db.commit()
    cursor.close()
    db.close()
    flash('Membership cancelled successfully!', 'success')
    return redirect(url_for('admin_members'))

@app.route('/view_trainers')
def view_trainers():
    trainers = get_trainers()
    return render_template('view_trainers.html', trainers=trainers)

if __name__ == '__main__':
    app.run(debug=True)
