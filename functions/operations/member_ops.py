import mysql.connector
from database.connection import connect_to_server

# ***********************
# REPORT / QUERY FUNCTIONS
# ***********************


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
    
def add_fee():
    print("\n--- Add Fee ---")
    status = input("Enter fee status (e.g., paid, due): ").strip()
    try:
        amount = float(input("Enter fee amount: ").strip())
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    semester = input("Enter semester(1st,2nd): ").strip()
    fee_name = input("Enter fee name: ").strip()
    academic_year = input("Enter academic year('2024-2025'): ").strip()
    try:
        membership_id = int(input("Enter membership ID: ").strip())
        organization_id = int(input("Enter organization ID: ").strip())
    except ValueError:
        print("Membership and organization IDs must be numeric.")
        return

    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO fee 
            (status, amount, due_date, semester, fee_name, academic_year, membership_id, organization_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (status, amount, due_date, semester, fee_name, academic_year, membership_id, organization_id))
        conn.commit()
        print("Fee Added successfully with payment number:", cursor.lastrowid)
    except Error as e:
        print("Error adding fee:", e)
    finally:
        cursor.close()
        conn.close()

def search_fee():
    print("\n--- Search Fee ---")
    try:
        payment_number = int(input("Enter payment number: ").strip())
    except ValueError:
        print("Payment number must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM fee WHERE payment_number = %s"
        cursor.execute(query, (payment_number,))
        result = cursor.fetchone()
        if result:
            print("\nFee record:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No fee record found with that payment number.")
    except Error as e:
        print("Error Searching fee:", e)
    finally:
        cursor.close()
        conn.close() 

def update_fee():
    print("\n--- Update Fee ---")
    try:
        payment_number = int(input("Enter payment number to update: ").strip())
    except ValueError:
        print("Invalid payment number. It must be numeric.")
        return
    new_status = input("Enter new fee status: ").strip()
    if not new_status:
        print("No new status provided.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "UPDATE fee SET status = %s WHERE payment_number = %s"
        cursor.execute(query, (new_status, payment_number))
        conn.commit()
        print("Fee updated successfully.")
    except Error as e:
        print("Error updating fee:", e)
    finally:
        cursor.close()
        conn.close()

def delete_fee():
    print("\n--- Delete Fee ---")
    try:
        payment_number = int(input("Enter payment number to delete: ").strip())
    except ValueError:
        print("Invalid payment number. It must be numeric.")
        return
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    cursor = conn.cursor()
    try:
        query = "DELETE FROM fee WHERE payment_number = %s"
        cursor.execute(query, (payment_number,))
        conn.commit()
        print("Fee deleted successfully.")
    except Error as e:
        print("Error deleting fee:", e)
    finally:
        cursor.close()
        conn.close() 


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
        conn.close()

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
