import mysql.connector
from database.connection import connect_to_server



def add_member_committee():
    print("\n--- Add Member_Committee Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        committee_id = int(input("Enter committee ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("Membership, committee, and organization IDs must be numeric.")
        return
    semester = input("Enter semester: ").strip()
    academic_year = input("Enter academic year: ").strip()
    role = input("Enter role: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO member_committee 
            (membership_id, committee_id, organization_id, semester, academic_year, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (membership_id, committee_id, organization_id, semester, academic_year, role))
        conn.commit()
        print("Member_Committee record addd successfully.")
    except Error as e:
        print("Error adding member_committee record:", e)
    finally:
        cursor.close()
        conn.close()

def search_member_committee():
    print("\n--- Search Member_Committee Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        committee_id = int(input("Enter committee ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    semester = input("Enter semester: ").strip()
    academic_year = input("Enter academic year: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT * FROM member_committee 
            WHERE membership_id = %s AND committee_id = %s AND organization_id = %s 
              AND semester = %s AND academic_year = %s
        """
        cursor.execute(query, (membership_id, committee_id, organization_id, semester, academic_year))
        result = cursor.fetchone()
        if result:
            print("\nMember_Committee record:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No record found with the given composite key.")
    except Error as e:
        print("Error searching member_committee record:", e)
    finally:
        cursor.close()
        conn.close()

def update_member_committee():
    print("\n--- Update Member_Committee Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        committee_id = int(input("Enter committee ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    semester = input("Enter semester: ").strip()
    academic_year = input("Enter academic year: ").strip()
    new_role = input("Enter new role: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
            UPDATE member_committee
            SET role = %s
            WHERE membership_id = %s AND committee_id = %s AND organization_id = %s
              AND semester = %s AND academic_year = %s
        """
        cursor.execute(query, (new_role, membership_id, committee_id, organization_id, semester, academic_year))
        conn.commit()
        print("Member_Committee record updated successfully.")
    except Error as e:
        print("Error updating member_committee record:", e)
    finally:
        cursor.close()
        conn.close()

def delete_member_committee():
    print("\n--- Delete Member_Committee Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        committee_id = int(input("Enter committee ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    semester = input("Enter semester: ").strip()
    academic_year = input("Enter academic year: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
            DELETE FROM member_committee
            WHERE membership_id = %s AND committee_id = %s AND organization_id = %s
              AND semester = %s AND academic_year = %s
        """
        cursor.execute(query, (membership_id, committee_id, organization_id, semester, academic_year))
        conn.commit()
        print("Member_Committee record deleted successfully.")
    except Error as e:
        print("Error deleting member_committee record:", e)
    finally:
        cursor.close()
        conn.close()