import mysql.connector
from database.connection import connect_to_server

def committee_menu():
    while True:
        print("\n--- Committee Management ---")
        print("1 - Add Committee")
        print("2 - View All Committees")
        print("3 - Update Committee")
        print("4 - Delete Committee")
        print("5 - Committee Member Management")
        print("0 - Back to Main Menu")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_committee()
        elif choice == '2':
            view_committees()
        elif choice == '3':
            update_committee()
        elif choice == '4':
            delete_committee()
        elif choice == '5':
            member_committee_menu()
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

def add_committee():
    print("\n--- Add Committee ---")
    committee_name = input("Enter committee name: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "INSERT INTO committee (committee_name) VALUES (%s)"
        cursor.execute(query, (committee_name,))
        conn.commit()
        print("Committee added successfully with ID:", cursor.lastrowid)
    except mysql.connector.Error as e:
        print("Error adding committee:", e)
    finally:
        cursor.close()
        conn.close()

def update_committee():
    print("\n--- Update Committee ---")
    try:
        committee_id = int(input("Enter committee ID to update: ").strip())
    except ValueError:
        print("Invalid committee ID.")
        return

    new_name = input("Enter new committee name: ").strip()

    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "UPDATE committee SET committee_name = %s WHERE committee_id = %s"
        cursor.execute(query, (new_name, committee_id))
        conn.commit()
        print("Committee updated successfully.")
    except mysql.connector.Error as e:
        print("Error updating committee:", e)
    finally:
        cursor.close()
        conn.close()

def view_committees():
    print("\n--- All Committees ---")
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM committee")
        results = cursor.fetchall()
        if results:
            for committee in results:
                print(f"\nCommittee ID: {committee['committee_id']}")
                print(f"  Name: {committee['committee_name']}")
        else:
            print("No committees found.")
    except mysql.connector.Error as e:
        print("Error retrieving committees:", e)
    finally:
        cursor.close()
        conn.close()

def delete_committee():
    print("\n--- Delete Committee ---")
    try:
        committee_id = int(input("Enter committee ID to delete: ").strip())
    except ValueError:
        print("Invalid committee ID.")
        return

    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "DELETE FROM committee WHERE committee_id = %s"
        cursor.execute(query, (committee_id,))
        conn.commit()
        print("Committee deleted successfully.")
    except mysql.connector.Error as e:
        print("Error deleting committee:", e)
    finally:
        cursor.close()
        conn.close()

def member_committee_menu():
    while True:
        print("\n--- Committee Member Management ---")
        print("1 - Add Member to Committee")
        print("2 - Search Committee Member Record")
        print("3 - Update Committee Member Role")
        print("4 - Delete Committee Member Record")
        print("0 - Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_member_committee()
        elif choice == '2':
            search_member_committee()
        elif choice == '3':
            update_member_committee()
        elif choice == '4':
            delete_member_committee()
        elif choice == '0':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


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