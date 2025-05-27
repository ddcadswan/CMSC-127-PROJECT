import mysql.connector
from database.connection import connect_to_server

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

def update_member():
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        print("Update member by:")
        print("1. Membership ID")
        print("2. Student Number")
        choice = input("Choose option 1 or 2: ").strip()

        if choice == "1":
            identifier_field = "membership_id"
            identifier_value = input("Enter Membership ID: ").strip()
        elif choice == "2":
            identifier_field = "student_number"
            identifier_value = input("Enter Student Number: ").strip()
        else:
            print("Invalid choice.")
            return

        # Fetch existing record
        cursor.execute(f"SELECT * FROM member WHERE {identifier_field} = %s;", (identifier_value,))
        member = cursor.fetchone()

        if not member:
            print("No member found with the given information.")
            return

        print("\nCurrent member details:")
        for key, value in member.items():
            print(f"{key}: {value}")

        print("\nEnter new values (press Enter to keep current value):")
        updated_fields = {}
        for field in ["first_name", "last_name", "student_number", "gender", "batch", "degree_program", "status", "role"]:
            current_value = member[field]
            new_value = input(f"{field.replace('_', ' ').title()} [{current_value}]: ").strip()
            if new_value:
                # Convert batch to int if modified
                updated_fields[field] = int(new_value) if field == "batch" else new_value

        if not updated_fields:
            print("No changes made.")
            return

        # Prepare update statement
        set_clause = ", ".join(f"{field} = %s" for field in updated_fields.keys())
        update_query = f"UPDATE member SET {set_clause} WHERE {identifier_field} = %s;"
        params = list(updated_fields.values()) + [identifier_value]
        cursor.execute(update_query, tuple(params))
        conn.commit()

        print("Member updated successfully!")

    except mysql.connector.Error as e:
        print("Error updating member:", e)
    except ValueError:
        print("Invalid input for batch. Please enter a valid year.")
    finally:
        cursor.close()
        conn.close()
