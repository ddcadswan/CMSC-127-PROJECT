# CMSC-127-PROJECT

### MySQL Setup Commands

```sql
-- Login to MySQL as root
mysql -u root -p;

-- Create a new user
CREATE USER 'student_admin'@'localhost' IDENTIFIED BY 'iLove127!';

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON *.* TO 'student_admin'@'localhost';
