CREATE DATABASE IF NOT EXISTS gym_db;
USE gym_db;

-- Table for Members
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    weight FLOAT,
    height FLOAT,
    reason VARCHAR(255),
    membership_plan VARCHAR(50),
    trainer_required BOOLEAN,
    trainer_id INT,
    start_date DATE,
    end_date DATE,
    total_amount DECIMAL(10,2)
);

-- Table for Trainers
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    experience INT,
    speciality VARCHAR(100)
);

-- Sample Trainers
INSERT INTO trainers (name, experience, speciality)
VALUES
('Amit Sharma', 5, 'Weight Training'),
('Priya Singh', 3, 'Yoga & Flexibility'),
('Rahul Patil', 7, 'Cardio & Endurance');
