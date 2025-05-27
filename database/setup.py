from .connection import connect_to_server
from mysql.connector import Error
# ***********************
# SETUP FUNCTIONS
# ***********************  

def setup_database():
    """
    Connects to the MySQL server, creates the database (if it does not exist),
    and creates the necessary tables according to the provided schema.
    """
    conn = connect_to_server()  # connect without specifying a database
    if not conn:
        print("Connection failed.")
        return
    cursor = conn.cursor()
    try:
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_org_database;")
        print("Database 'student_org_database' created or already exists.")
        # Switch to the new database
        conn.database = "student_org_database"

        # Create the tables
        create_member = """
        CREATE TABLE IF NOT EXISTS member (
            membership_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            student_number VARCHAR(20) UNIQUE NOT NULL,
            gender VARCHAR(10),
            batch INT,
            degree_program VARCHAR(100),
            status VARCHAR(20),
            role VARCHAR(30)
        );
        """
        cursor.execute(create_member)

        create_organization = """
        CREATE TABLE IF NOT EXISTS organization (
            org_id INT PRIMARY KEY AUTO_INCREMENT,
            org_name VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_organization)

        create_fee = """
        CREATE TABLE IF NOT EXISTS fee (
            payment_number INT PRIMARY KEY AUTO_INCREMENT,
            status VARCHAR(20),
            amount DECIMAL(10, 2),
            due_date DATE,
            semester VARCHAR(10),
            fee_name VARCHAR(50),
            academic_year VARCHAR(20),
            membership_id INT,
            organization_id INT,
            FOREIGN KEY (membership_id) REFERENCES member (membership_id),
            FOREIGN KEY (organization_id) REFERENCES organization (org_id)
        );
        """
        cursor.execute(create_fee)

        create_committee = """
        CREATE TABLE IF NOT EXISTS committee (
            committee_id INT PRIMARY KEY AUTO_INCREMENT,
            committee_name VARCHAR(100)
        );
        """
        cursor.execute(create_committee)

        create_member_committee = """
        CREATE TABLE IF NOT EXISTS member_committee (
            membership_id INT,
            committee_id INT,
            organization_id INT,
            semester VARCHAR(10),
            academic_year VARCHAR(20),
            role VARCHAR(30),
            PRIMARY KEY (membership_id, committee_id, organization_id, semester, academic_year),
            FOREIGN KEY (membership_id) REFERENCES member(membership_id),
            FOREIGN KEY (committee_id) REFERENCES committee (committee_id),
            FOREIGN KEY (organization_id) REFERENCES organization (org_id)
        );
        """
        cursor.execute(create_member_committee)

        create_membership = """
        CREATE TABLE IF NOT EXISTS membership (
            membership_id INT,
            organization_id INT,
            PRIMARY KEY (membership_id, organization_id),
            FOREIGN KEY (membership_id) REFERENCES member(membership_id),
            FOREIGN KEY (organization_id) REFERENCES organization(org_id)
        );
        """
        cursor.execute(create_membership)

        conn.commit()
        print("All tables created successfully!")
    except Error as e:
        print("Error during setup:", e)
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """
    Inserts sample data into the tables for organizations, committees, members,
    memberships, fees, and member_committee as provided in the SQL script.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Insert Organizations
        cursor.execute("INSERT INTO organization (org_name) VALUES ('Computer Science Society');")
        cursor.execute("INSERT INTO organization (org_name) VALUES ('Association of Computer Studies Students');")

        # Insert Committees
        cursor.execute("INSERT INTO committee (committee_name) VALUES ('Events');")
        cursor.execute("INSERT INTO committee (committee_name) VALUES ('Finance');")

        # Insert Members
        insert_member_query = """
        INSERT INTO member (first_name, last_name, student_number, gender, batch, degree_program, status, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        members = [
            ('Alice', 'Guo', '202156789', 'Female', 2021, 'BS Computer Science', 'active', 'President'),
            ('Bob', 'Builder', '202198765', 'Male', 2021, 'BS Computer Science', 'active', 'Vice President'),
            ('Charlie', 'Puth', '202277658', 'Male', 2022, 'BS Computer Science', 'inactive', 'Member'),
            ('Ana', 'Lim', '2022345678', 'Female', 2022, 'BS Computer Science', 'active', 'Treasurer'),
            ('Eli', 'Yu', '202323478', 'Other', 2023, 'BS Computer Science', 'active', 'Member')
        ]
        cursor.executemany(insert_member_query, members)

        # Insert Memberships
        # Here we assume that the auto-increment values for members are 1, 2, 3, 4, 5 respectively.
        memberships = [
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 2),
            (5, 1)
        ]
        for membership in memberships:
            cursor.execute("INSERT INTO membership (membership_id, organization_id) VALUES (%s, %s);", membership)

        # Insert Fees
        fee_insert_query = """
        INSERT INTO fee (status, amount, due_date, semester, fee_name, academic_year, membership_id, organization_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        fee_data = [
            ('paid', 500.00, '2025-03-15', '2nd', 'Annual Dues', '2024-2025', 1, 1),
            ('unpaid', 500.00, '2025-03-15', '2nd', 'Annual Dues', '2024-2025', 2, 1),
            ('late', 600.00, '2025-03-01', '2nd', 'Activity Fee', '2024-2025', 4, 2)
        ]
        cursor.executemany(fee_insert_query, fee_data)

        # Insert Member Committees
        mc_insert_query = """
        INSERT INTO member_committee (membership_id, committee_id, organization_id, semester, academic_year, role)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        mc_data = [
            (1, 1, 1, '2nd', '2024-2025', 'Chair'),
            (2, 1, 1, '2nd', '2024-2025', 'Member'),
            (4, 2, 2, '2nd', '2024-2025', 'Treasurer')
        ]
        cursor.executemany(mc_insert_query, mc_data)

        conn.commit()
        print("Sample data inserted successfully!")
    except Error as e:
        print("Error inserting sample data:", e)
    finally:
        cursor.close()
        conn.close()

