CREATE DATABASE IF NOT EXISTS gym_db;
USE gym_db;

-- Table for Admin Users
CREATE TABLE admin_users (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('super_admin', 'admin', 'staff') DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Table for Members
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    age INT,
    weight FLOAT,
    height FLOAT,
    reason VARCHAR(255),
    membership_plan VARCHAR(50),
    trainer_required BOOLEAN DEFAULT FALSE,
    trainer_id INT,
    start_date DATE,
    end_date DATE,
    total_amount DECIMAL(10,2),
    status ENUM('active', 'expired', 'suspended', 'cancelled') DEFAULT 'active',
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(15),
    address TEXT,
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id) ON DELETE SET NULL
);

-- Table for Trainers
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    experience INT,
    speciality VARCHAR(100),
    bio TEXT,
    hourly_rate DECIMAL(8,2),
    profile_image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Membership Plans
CREATE TABLE membership_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL,
    duration_days INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    trainer_price DECIMAL(10,2) DEFAULT 0,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Payments
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_type ENUM('membership', 'trainer', 'class', 'equipment', 'other') NOT NULL,
    payment_method ENUM('cash', 'card', 'upi', 'bank_transfer', 'cheque') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    notes TEXT,
    created_by INT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES admin_users(admin_id) ON DELETE SET NULL
);

-- Table for Attendance
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    check_out_time TIMESTAMP NULL,
    duration_minutes INT DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Table for Classes
CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    description TEXT,
    trainer_id INT,
    max_capacity INT DEFAULT 20,
    duration_minutes INT DEFAULT 60,
    price DECIMAL(8,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id) ON DELETE SET NULL
);

-- Table for Class Schedules
CREATE TABLE class_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    schedule_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_cancelled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

-- Table for Class Bookings
CREATE TABLE class_bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    schedule_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('booked', 'cancelled', 'completed', 'no_show') DEFAULT 'booked',
    payment_id INT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES class_schedules(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (payment_id) REFERENCES payments(payment_id) ON DELETE SET NULL
);

-- Table for Equipment
CREATE TABLE equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    model VARCHAR(50),
    serial_number VARCHAR(100),
    purchase_date DATE,
    purchase_price DECIMAL(10,2),
    status ENUM('active', 'maintenance', 'out_of_order', 'retired') DEFAULT 'active',
    location VARCHAR(100),
    last_maintenance DATE,
    next_maintenance DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Equipment Maintenance
CREATE TABLE equipment_maintenance (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL,
    maintenance_type ENUM('routine', 'repair', 'inspection') NOT NULL,
    description TEXT,
    cost DECIMAL(8,2),
    maintenance_date DATE NOT NULL,
    next_maintenance_date DATE,
    technician VARCHAR(100),
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE
);

-- Table for Notifications
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Table for System Settings
CREATE TABLE system_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert Sample Data

-- Sample Admin Users
INSERT INTO admin_users (username, email, password_hash, full_name, role) VALUES
('admin', 'admin@mkcfitness.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K8K8K8', 'System Administrator', 'super_admin'),
('staff1', 'staff1@mkcfitness.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K8K8K8', 'John Staff', 'staff');

-- Sample Trainers
INSERT INTO trainers (name, email, phone, experience, speciality, bio, hourly_rate) VALUES
('Amit Sharma', 'amit@mkcfitness.com', '+91-9876543210', 5, 'Weight Training', 'Certified personal trainer with 5 years of experience in strength training and bodybuilding.', 1500.00),
('Priya Singh', 'priya@mkcfitness.com', '+91-9876543211', 3, 'Yoga & Flexibility', 'Yoga instructor specializing in Hatha and Vinyasa yoga for all fitness levels.', 1200.00),
('Rahul Patil', 'rahul@mkcfitness.com', '+91-9876543212', 7, 'Cardio & Endurance', 'Expert in cardiovascular training, HIIT, and endurance sports preparation.', 1800.00),
('Sneha Gupta', 'sneha@mkcfitness.com', '+91-9876543213', 4, 'Pilates & Core', 'Pilates instructor focused on core strength and postural alignment.', 1400.00);

-- Sample Membership Plans
INSERT INTO membership_plans (plan_name, duration_days, price, trainer_price, description) VALUES
('1 Month', 30, 1000.00, 500.00, 'Basic monthly membership with gym access'),
('3 Months', 90, 2500.00, 1200.00, 'Quarterly membership with 10% discount'),
('6 Months', 180, 4500.00, 2000.00, 'Half-yearly membership with 15% discount'),
('1 Year', 365, 8000.00, 3500.00, 'Annual membership with 20% discount and premium benefits');

-- Sample Classes
INSERT INTO classes (class_name, description, trainer_id, max_capacity, duration_minutes, price) VALUES
('Morning Yoga', 'Gentle yoga session to start your day', 2, 15, 60, 200.00),
('HIIT Cardio', 'High-intensity interval training for maximum calorie burn', 3, 20, 45, 300.00),
('Weight Training Basics', 'Introduction to proper weight training techniques', 1, 12, 90, 400.00),
('Pilates Core', 'Core strengthening and flexibility session', 4, 18, 60, 250.00);

-- Sample Equipment
INSERT INTO equipment (equipment_name, category, brand, model, status, location, last_maintenance) VALUES
('Treadmill Pro', 'Cardio', 'Life Fitness', 'T5', 'active', 'Cardio Zone', '2024-01-15'),
('Dumbbell Set', 'Strength', 'York', 'Professional', 'active', 'Weight Room', '2024-01-10'),
('Yoga Mats', 'Accessories', 'Lululemon', 'The Reversible', 'active', 'Yoga Studio', '2024-01-20'),
('Elliptical Machine', 'Cardio', 'Precor', 'EFX 835', 'active', 'Cardio Zone', '2024-01-12');

-- Sample System Settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('gym_name', 'MKC Fitness Center', 'Name of the gym'),
('gym_address', '123 Fitness Street, Pune, Maharashtra 411001', 'Gym address'),
('gym_phone', '+91-20-12345678', 'Gym contact number'),
('gym_email', 'info@mkcfitness.com', 'Gym email address'),
('membership_auto_renewal', 'false', 'Enable automatic membership renewal'),
('max_daily_attendance', '100', 'Maximum daily attendance limit'),
('class_booking_advance_days', '7', 'Days in advance members can book classes');
