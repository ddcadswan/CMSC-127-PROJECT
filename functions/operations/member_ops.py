import mysql.connector
from database.connection import connect_to_server

def add_member():
    print("\n--- Add Member ---")
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    student_number = input("Enter student number: ").strip()
    gender = input("Enter gender: ").strip()
    try:
        batch = int(input("Enter batch (year): ").strip())
    except ValueError:
        print("Invalid batch. Please enter a numeric year.")
        return
    degree_program = input("Enter degree program: ").strip()
    status = input("Enter status (e.g., active/inactive): ").strip()
    role = input("Enter role: ").strip()
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO member 
            (first_name, last_name, student_number, gender, batch, degree_program, status, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, student_number, gender, batch, degree_program, status, role))
        conn.commit()
        print("Member Added successfully with ID:", cursor.lastrowid)
    except Error as e:
        print("Error adding member:", e)
    finally:
        cursor.close()
        conn.close()
def update_member():
    print("\n--- Update Member ---")
    try:
        membership_id = int(input("Enter membership ID to update: ").strip())
    except ValueError:
        print("Invalid membership ID. It must be numeric.")
        return
    update_fields = {}
    print("Enter new values for update (leave blank to skip):")
    new_status = input("New status (active/inactive): ").strip()
    new_role = input("New role: ").strip()
    if new_status:
        update_fields["status"] = new_status
    if new_role:
        update_fields["role"] = new_role
    if not update_fields:
        print("No updates provided.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        set_clause = ", ".join([f"{col} = %s" for col in update_fields.keys()])
        values = list(update_fields.values())
        values.append(membership_id)
        query = f"UPDATE member SET {set_clause} WHERE membership_id = %s"
        cursor.execute(query, tuple(values))
        conn.commit()
        print("Member updated successfully.")
    except Error as e:
        print("Error updating member:", e)
    finally:
        cursor.close()
        conn.close()
def delete_member():
    print("\n--- Delete Member ---")
    try:
        membership_id = int(input("Enter membership ID to delete: ").strip())
    except ValueError:
        print("Invalid membership ID. It must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "DELETE FROM member WHERE membership_id = %s"
        cursor.execute(query, (membership_id,))
        conn.commit()
        print("Member deleted successfully.")
    except Error as e:
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
        membership_id = input("Membership id: ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        student_number = input("Student Number: ").strip()

        conditions = []
        params = []
        if membership_id:
            conditions.append("membership_id LIKE %s")
            params.append(f"%{membership_id}%")
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
