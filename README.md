# CMSC-127-PROJECT

## What is the Application?
This is an information system for Student Organizations. Built and designed for the management and tracking of 
student organization's operations, like memberships and finances.

## How to Run

1. MySQL Setup Commands

sql
-- Login to MySQL as root
mysql -u root -p;

-- Create a new user
CREATE USER 'student_admin'@'localhost' IDENTIFIED BY 'iLove127!';

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON *.* TO 'student_admin'@'localhost';

2. Run gui.py to start the application
3. Click the 'Setup Database & Tables' and 'Insert Sample Data' 
4. Explore
