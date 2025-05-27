from database.connection import connect_to_server
from mysql.connector import Error

# ***********************
# REPORT / QUERY FUNCTIONS
# ***********************
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

