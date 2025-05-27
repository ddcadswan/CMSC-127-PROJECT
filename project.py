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

# ***********************
# REPORT / QUERY FUNCTIONS
# ***********************


def add_member():
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        print("Enter new member details:")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        student_number = input("Student Number: ").strip()
        gender = input("Gender: ").strip()
        batch = int(input("Batch (year): ").strip())
        degree_program = input("Degree Program: ").strip()
        status = input("Status (active/inactive): ").strip()
        role = input("Role: ").strip()

        insert_query = """
        INSERT INTO member (first_name, last_name, student_number, gender, batch, degree_program, status, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (first_name, last_name, student_number, gender, batch, degree_program, status, role))
        conn.commit()
        print("Member added successfully!")
    except mysql.connector.Error as e:
        print("Error adding member:", e)
    finally:
        cursor.close()
        conn.close()

def delete_member():
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        print("Delete member by:")
        print("1. Membership ID")
        print("2. Student Number")
        choice = input("Choose option 1 or 2: ").strip()

        if choice == "1":
            membership_id = input("Enter Membership ID: ").strip()
            cursor.execute("DELETE FROM member WHERE membership_id = %s;", (membership_id,))
        elif choice == "2":
            student_number = input("Enter Student Number: ").strip()
            cursor.execute("DELETE FROM member WHERE student_number = %s;", (student_number,))
        else:
            print("Invalid choice.")
            return

        conn.commit()
        if cursor.rowcount > 0:
            print("Member deleted successfully!")
        else:
            print("No member found with the given information.")
    except mysql.connector.Error as e:
        print("Error deleting member:", e)
    finally:
        cursor.close()
        conn.close()

def search_members():
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        print("Search members by (leave blank to skip a criterion):")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        student_number = input("Student Number: ").strip()

        conditions = []
        params = []

        if first_name:
            conditions.append("first_name LIKE %s")
            params.append(f"%{first_name}%")
        if last_name:
            conditions.append("last_name LIKE %s")
            params.append(f"%{last_name}%")
        if student_number:
            conditions.append("student_number LIKE %s")
            params.append(f"%{student_number}%")

        if not conditions:
            print("No search criteria entered.")
            return

        query = "SELECT membership_id, first_name, last_name, student_number, gender, batch, degree_program, status, role FROM member WHERE " + " AND ".join(conditions) + ";"
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        if results:
            print("\nSearch results:")
            for row in results:
                print(row)
        else:
            print("No members matched your search criteria.")
    except mysql.connector.Error as e:
        print("Error searching members:", e)
    finally:
        cursor.close()
        conn.close()
def view_all_students():
    """
    Displays all members belonging to a specified organization.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query= """
        SELECT * FROM member
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print(f"\nMembers in Organization:")
            for row in results:
                print(row)
        else:
            print("No members found for the entered organization.")
    except Error as e:
        print("Error querying members:", e)
    finally:
        cursor.close()
        conn.close()
def sorted_by(org_id,sort_by):
    if sort_by == "1":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role,m.degree_program,m.gender
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE o.org_id = %s
        ORDER BY m.role;
        """
    elif sort_by == "2":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role,m.degree_program,m.gender
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE o.org_id = %s
        ORDER BY m.status;
        """
    elif sort_by == "3":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role,m.degree_program,m.gender
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE o.org_id = %s
        ORDER BY m.gender;
        """
    elif sort_by == "4":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role,m.degree_program,m.gender
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE o.org_id = %s
        ORDER BY m.degree_program;
        """
    elif sort_by == "5":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role,m.degree_program,m.gender
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE o.org_id = %s
        ORDER BY m.batch;
        """
    elif sort_by == "6":
        query = """
        SELECT o.org_name, m.first_name, m.last_name, m.student_number, m.status, m.role, m.degree_program, m.gender, c.committee_name
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        LEFT JOIN member_committee mc ON mc.membership_id = m.membership_id AND mc.organization_id = o.org_id
        LEFT JOIN committee c ON mc.committee_id = c.committee_id
        WHERE o.org_id = %s
        ORDER BY c.committee_name;
        """

    return query, (org_id,)
def view_all_members():
    """
    Displays all members belonging to a specified organization.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        org_id = input("Enter Organization ID to view all members: ")
        sort_by = input(
            """
            ================================================================
            Sort by:
            1 - role
            2 - status
            3 - gender
            4 - degree program
            5 - batch
            6 - commitee
            ===================================================================
            """)
        query, params = sorted_by(org_id,sort_by)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            print(f"\nMembers in Organization ID {org_id}:")
            for row in results:
                print(row)
        else:
            print("No members found for the entered organization.")
    except Error as e:
        print("Error querying members:", e)
    finally:
        cursor.close()
        conn.close()

def view_members_unpaid_fees():
    """
    Displays members with unpaid or late fees for a given semester and academic year.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        semester = input("Enter Semester (e.g., '2nd'): ")
        academic_year = input("Enter Academic Year (e.g., '2024-2025'): ")
        query = """
        SELECT m.first_name, m.last_name, o.org_name, f.status, f.amount, f.semester, f.academic_year
        FROM fee f
        JOIN member m ON f.membership_id = m.membership_id
        JOIN organization o ON f.organization_id = o.org_id
        WHERE f.status IN ('unpaid', 'late')
          AND f.semester = %s
          AND f.academic_year = %s;
        """
        cursor.execute(query, (semester, academic_year))
        results = cursor.fetchall()
        if results:
            print("\nMembers with unpaid or late fees:")
            for row in results:
                print(row)
        else:
            print("No unpaid fees records found for the given criteria.")
    except Error as e:
        print("Error querying unpaid fees:", e)
    finally:
        cursor.close()
        conn.close()

def view_member_orgs():
    """
    Given a membership id, displays all organizations to which the member is registered.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        membership_id = input("Enter Membership ID to check all organizations: ")
        query = """
        SELECT m.first_name, m.last_name, o.org_name
        FROM membership ms
        JOIN member m ON ms.membership_id = m.membership_id
        JOIN organization o ON ms.organization_id = o.org_id
        WHERE m.membership_id = %s;
        """
        cursor.execute(query, (membership_id,))
        results = cursor.fetchall()
        if results:
            print(f"\nOrganizations for Membership ID {membership_id}:")
            for row in results:
                print(row)
        else:
            print("No organizations found for this member.")
    except Error as e:
        print("Error querying member organizations:", e)
    finally:
        cursor.close()
        conn.close()

def view_member_unpaid_fees():
    """
    Given a student number, shows the member's unpaid fees across all organizations.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        student_number = input("Enter Student Number: ")
        query = """
        SELECT m.first_name, m.last_name, o.org_name, f.fee_name, f.amount, f.status, f.semester, f.academic_year
        FROM member m
        JOIN fee f ON m.membership_id = f.membership_id
        JOIN organization o ON f.organization_id = o.org_id
        WHERE m.student_number = %s
          AND f.status IN ('unpaid', 'late');
        """
        cursor.execute(query, (student_number,))
        results = cursor.fetchall()
        if results:
            print(f"\nUnpaid or late fees for Student Number {student_number}:")
            for row in results:
                print(row)
        else:
            print("No unpaid fee records found for this student.")
    except Error as e:
        print("Error querying member unpaid fees:", e)
    finally:
        cursor.close()
        conn.close()

def list_active_members():
    """
    Lists all active members from the members table.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "SELECT first_name, last_name, degree_program FROM member WHERE status = 'active';"
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nActive Members:")
            for row in results:
                print(row)
        else:
            print("No active members found.")
    except Error as e:
        print("Error querying active members:", e)
    finally:
        cursor.close()
        conn.close()

def view_members_with_unpaid_or_late():
    """
    Displays members who have unpaid or late fees.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
        SELECT m.first_name, m.last_name, f.status, f.amount
        FROM member m
        JOIN fee f ON m.membership_id = f.membership_id
        WHERE f.status IN ('unpaid', 'late');
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nMembers with unpaid or late fees:")
            for row in results:
                *others, last = row  # Unpack all but the last item into `others`, last item into `last`
                print(*others, f"{float(last):.2f}")

        else:
            print("No records of unpaid or late fees found.")
    except Error as e:
        print("Error querying unpaid or late fees:", e)
    finally:
        cursor.close()
        conn.close()

def view_committee_roles():
    """
    Shows the roles of members within committees for each organization.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
        SELECT m.first_name, m.last_name, o.org_name, c.committee_name, mc.role
        FROM member m
        JOIN member_committee mc ON m.membership_id = mc.membership_id
        JOIN organization o ON mc.organization_id = o.org_id
        JOIN committee c ON mc.committee_id = c.committee_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nCommittee roles per organization:")
            for row in results:
                print(row)
        else:
            print("No committee roles found.")
    except Error as e:
        print("Error querying committee roles:", e)
    finally:
        cursor.close()
        conn.close()

def view_total_fee_collected():
    """
    Displays the total fee amount collected (only for paid fees) per organization.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
        SELECT o.org_name, SUM(f.amount) AS total_collected
        FROM fee f
        JOIN organization o ON f.organization_id = o.org_id
        WHERE f.status = 'paid'
        GROUP BY o.org_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nTotal fee amount collected per organization:")
            for row in results:
                *others, last = row
                print(*others, f"{float(last):.2f}")

        else:
            print("No fee collection data found.")
    except Error as e:
        print("Error querying fee collection:", e)
    finally:
        cursor.close()
        conn.close()

def view_member_count():
    """
    Displays the number of members per organization.
    """
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
        SELECT o.org_name, COUNT(ms.membership_id) AS member_count
        FROM membership ms
        JOIN organization o ON ms.organization_id = o.org_id
        GROUP BY o.org_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nNumber of members per organization:")
            for row in results:
                print(row)
        else:
            print("No data on member counts found.")
    except Error as e:
        print("Error querying member counts:", e)
    finally:
        cursor.close()
        conn.close()

def print_report_menu():
    while True:
        print("============================================================================")
        print("\t1. View number of members per organization")
        print("\t2. View all members of an organization")
        print("\t3. View members with unpaid or late fees (by semester & academic year)")
        print("\t4. View organizations of a member (by membership ID)")
        print("\t5. View a member's unpaid fees (by student number)")
        print("\t6. List all active members")
        print("\t7. View members with unpaid or late fees")
        print("\t8. View committee roles per organization")
        print("\t9. View total fee amount collected per organization")
        print("\t10. View all students")
        print("\t0 - Exit")
        print

        choice = input("Choose an option: ").strip()
      
        if choice == "1":
           view_member_count()
        elif choice == "2":
            view_all_members()
        elif choice == "3":
            view_members_unpaid_fees()
        elif choice == "4":
            view_member_orgs()
        elif choice == "5":
            view_member_unpaid_fees()
        elif choice == "6":
            list_active_members()
        elif choice == "7":
            view_members_with_unpaid_or_late()
        elif choice == "8":
            view_committee_roles()
        elif choice == "9":
            view_total_fee_collected()
        elif choice == "10":
            view_all_students()
        elif choice == "0":
            print("Back to main menu")
            break
        else:
            print("Invalid option, please try again.")

# ***********************
# MENU AND MAIN LOOP
# ***********************

def main():
    while True:
        print("\n=== Student Organization Management ===")
        print("99 - Setup Database & Tables")
        print("1 - Insert Sample Data")
        print("2 - Add Member")
        print("3 - Search Options")
        print("4 - Delete Member")
        print("5 - Generate Report")
        print("0 - Exit")

        choice = input("Choose an option: ").strip()

        if choice == "99":
            setup_database()
        elif choice == "1":
            insert_sample_data()
        elif choice == "2":
            add_member()
        elif choice == "3":
            search_members()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            print_report_menu()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

