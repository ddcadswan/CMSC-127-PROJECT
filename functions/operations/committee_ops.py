import mysql.connector
from database.connection import connect_to_server

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
    except Error as e:
        print("Error adding committee:", e)
    finally:
        cursor.close()
        conn.close()

def search_committee():
    print("\n--- Search Committee ---")
    try:
        committee_id = int(input("Enter committee ID: ").strip())
    except ValueError:
        print("Committee ID must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM committee WHERE committee_id = %s"
        cursor.execute(query, (committee_id,))
        result = cursor.fetchone()
        if result:
            print("\nCommittee record:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No committee found with that ID.")
    except Error as e:
        print("Error Searching committee:", e)
    finally:
        cursor.close()
        conn.close()

def update_committee():
    print("\n--- Update Committee ---")
    try:
        committee_id = int(input("Enter committee ID to update: ").strip())
    except ValueError:
        print("Committee ID must be numeric.")
        return
    new_committee_name = input("Enter new committee name: ").strip()
    if not new_committee_name:
        print("No new committee name provided.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "UPDATE committee SET committee_name = %s WHERE committee_id = %s"
        cursor.execute(query, (new_committee_name, committee_id))
        conn.commit()
        print("Committee updated successfully.")
    except Error as e:
        print("Error updating committee:", e)
    finally:
        cursor.close()
        conn.close()

def delete_committee():
    print("\n--- Delete Committee ---")
    try:
        committee_id = int(input("Enter committee ID to delete: ").strip())
    except ValueError:
        print("Committee ID must be numeric.")
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
    except Error as e:
        print("Error deleting committee:", e)
    finally:
        cursor.close()
        conn.clos