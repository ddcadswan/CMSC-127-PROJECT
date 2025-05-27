import mysql.connector
from database.connection import connect_to_server

def add_membership():
    print("\n--- add Membership Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "INSERT INTO membership (membership_id, organization_id) VALUES (%s, %s)"
        cursor.execute(query, (membership_id, organization_id))
        conn.commit()
        print("Membership record added successfully.")
    except Error as e:
        print("Error adding membership record:", e)
    finally:
        cursor.close()
        conn.close()

def search_membership():
    print("\n--- Search Membership Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM membership WHERE membership_id = %s AND organization_id = %s"
        cursor.execute(query, (membership_id, organization_id))
        result = cursor.fetchone()
        if result:
            print("\nMembership record:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No membership record found.")
    except Error as e:
        print("Error searching membership record:", e)
    finally:
        cursor.close()
        conn.close()

def delete_membership():
    print("\n--- Delete Membership Record ---")
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("IDs must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "DELETE FROM membership WHERE membership_id = %s AND organization_id = %s"
        cursor.execute(query, (membership_id, organization_id))
        conn.commit()
        print("Membership record deleted successfully.")
    except Error as e:
        print("Error deleting membership record:", e)
    finally:
        cursor.close()
        conn.close()
