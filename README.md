# CMSC-127-PROJECT

### MySQL Setup Commands

```sql
-- Login to MySQL as root
mysql -u root -p;

-- Create a new user
CREATE USER 'student_admin'@'localhost' IDENTIFIED BY 'iLove127!';

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON *.* TO 'student_admin'@'localhost';

### HOW TO RUN
- python main.py
- mysql -u student_admin -piLove127!

NOTE: Setup database first as seen in the menu.


## Tkinter References
- GUI Reference [link](https://docs.python.org/3/library/tkinter.html)
- Tkinter elements [link](https://realpython.com/python-gui-tkinter/)