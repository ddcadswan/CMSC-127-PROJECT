import mysql.connector
from mysql.connector import Error

# Function to connect to MySQL.
# If no database is specified the connection is made to the server only.
def connect_to_server(database=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="student_admin",
            password="iLove127!",
            database=database
        )
        if conn.is_connected():
            db_msg = f" Database: {database}" if database else ""
            print("Connected to MySQL Server" + db_msg)
            return conn
    except Error as e:
        print("Error while connecting to MySQL:", e)
    return None