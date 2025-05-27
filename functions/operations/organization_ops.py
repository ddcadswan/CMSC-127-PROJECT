import mysql.connector
from database.connection import connect_to_server
   
def add_organization():
    print("\n--- Add Organization ---")
    org_name = input("Enter organization name: ").strip()
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "INSERT INTO organization (org_name) VALUES (%s)"
        cursor.execute(query, (org_name,))
        conn.commit()
        print("Organization Added successfully with ID:", cursor.lastrowid)
    except Error as e:
        print("Error adding organization:", e)
    finally:
        cursor.close()
        conn.close()

def search_organization():
    print("\n--- Search Organization ---")
    try:
        org_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("Invalid organization ID. It must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM organization WHERE org_id = %s"
        cursor.execute(query, (org_id,))
        result = cursor.fetchone()
        if result:
            print("\nOrganization data:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No organization found with that ID.")
    except Error as e:
        print("Error Searching organization:", e)
    finally:
        cursor.close()
        conn.close()

def update_organization():
    print("\n--- Update Organization ---")
    try:
        org_id = int(input("Enter organization ID to update: ").strip())
    except ValueError:
        print("Invalid organization ID. It must be numeric.")
        return
    new_org_name = input("Enter new organization name: ").strip()
    if not new_org_name:
        print("No new organization name provided.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "UPDATE organization SET org_name = %s WHERE org_id = %s"
        cursor.execute(query, (new_org_name, org_id))
        conn.commit()
        print("Organization updated successfully.")
    except Error as e:
        print("Error updating organization:", e)
    finally:
        cursor.close()
        conn.close()

def delete_organization():
    print("\n--- Delete Organization ---")
    try:
        org_id = int(input("Enter organization ID to delete: ").strip())
    except ValueError:
        print("Invalid organization ID. It must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "DELETE FROM organization WHERE org_id = %s"
        cursor.execute(query, (org_id,))
        conn.commit()
        print("Organization deleted successfully.")
    except Error as e:
        print("Error deleting organization:", e)
    finally:
        cursor.close()
        conn.close()
    