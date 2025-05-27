import mysql.connector
from database.connection import connect_to_server
   
def organization_menu():
    while True:
        print("\n====== Organization Management ======")
        print("1 - Add Organization")
        print("2 - Add Member to Organization") 
        print("3 - Update Organization")
        print("4 - Delete Organization")
        print("5 - Search Organization")
        print("0 - Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_organization()
        elif choice == '2':
            add_member_to_organization()
        elif choice == '3':
            update_organization()
        elif choice == '4':
            delete_organization()
        elif choice == '5':
            search_organization()
        elif choice == '0':
            print("Returning to main menu...")
            break
        else:
            print("Invalid option. Please select a number between 1 and 6.")

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

def add_member_to_organization():
    print("\n--- Add Member to Organization ---")
    
    conn = connect_to_server("student_org_database")
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Show available organizations
        print("\nAvailable Organizations:")
        cursor.execute("SELECT org_id, org_name FROM organization")
        organizations = cursor.fetchall()
        
        if not organizations:
            print("No organizations found. Please add an organization first.")
            return
        
        for org in organizations:
            print(f"  {org['org_id']} - {org['org_name']}")
        
        # Get organization ID
        try:
            org_id = int(input("\nEnter organization ID: ").strip())
        except ValueError:
            print("Invalid organization ID. It must be numeric.")
            return
        
        # Verify organization exists
        cursor.execute("SELECT org_name FROM organization WHERE org_id = %s", (org_id,))
        org_result = cursor.fetchone()
        if not org_result:
            print("Organization not found.")
            return
        
        print(f"\nAdding member to: {org_result['org_name']}")
        
        # Show available members who are NOT already in this organization
        print("\nAvailable Members:")
        query = """
        SELECT m.membership_id, m.first_name, m.last_name, m.student_number, m.degree_program, m.batch
        FROM member m
        WHERE m.membership_id NOT IN (
            SELECT ms.membership_id 
            FROM membership ms 
            WHERE ms.organization_id = %s
        )
        ORDER BY m.last_name, m.first_name
        """
        cursor.execute(query, (org_id,))
        available_members = cursor.fetchall()
        
        if not available_members:
            print("No available members to add. All existing members are already in this organization.")
            return
        
        print("\nID   | Name                    | Student Number | Degree Program      | Batch")
        print("-" * 80)
        for member in available_members:
            name = f"{member['first_name']} {member['last_name']}"
            degree = member['degree_program'] or "N/A"
            batch = str(member['batch']) if member['batch'] else "N/A"
            print(f"{member['membership_id']:<4} | {name:<23} | {member['student_number']:<14} | {degree:<19} | {batch}")
        
        # Get member selection
        try:
            membership_id = int(input("\nEnter member ID to add to organization: ").strip())
        except ValueError:
            print("Invalid member ID. It must be numeric.")
            return
        
        # Verify member exists and is available
        member_found = False
        selected_member = None
        for member in available_members:
            if member['membership_id'] == membership_id:
                member_found = True
                selected_member = member
                break
        
        if not member_found:
            print("Invalid member ID or member is already in this organization.")
            return
        
        # Create membership relationship
        membership_query = "INSERT INTO membership (membership_id, organization_id) VALUES (%s, %s)"
        cursor.execute(membership_query, (membership_id, org_id))
        
        conn.commit()
        print(f"\nSuccess! {selected_member['first_name']} {selected_member['last_name']} has been added to '{org_result['org_name']}'!")
        
    except Error as e:
        print("Error adding member to organization:", e)
        conn.rollback()
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
        # Get organization details
        query = "SELECT * FROM organization WHERE org_id = %s"
        cursor.execute(query, (org_id,))
        result = cursor.fetchone()
        
        if not result:
            print("No organization found with that ID.")
            return
        
        print("\n" + "="*60)
        print("ORGANIZATION DETAILS")
        print("="*60)
        for key, value in result.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Get organization members
        members_query = """
        SELECT m.membership_id, m.first_name, m.last_name, m.student_number, 
               m.gender, m.batch, m.degree_program, m.status, m.role
        FROM member m
        INNER JOIN membership ms ON m.membership_id = ms.membership_id
        WHERE ms.organization_id = %s
        ORDER BY m.last_name, m.first_name
        """
        cursor.execute(members_query, (org_id,))
        members = cursor.fetchall()
        
        print(f"\n" + "="*60)
        print(f"ORGANIZATION MEMBERS ({len(members)} total)")
        print("="*60)
        
        if members:
            print("\nID   | Name                    | Student Number | Role         | Status    | Batch | Gender")
            print("-" * 95)
            for member in members:
                name = f"{member['first_name']} {member['last_name']}"
                role = member['role'] or "N/A"
                status = member['status'] or "N/A"
                batch = str(member['batch']) if member['batch'] else "N/A"
                gender = member['gender'] or "N/A"
                print(f"{member['membership_id']:<4} | {name:<23} | {member['student_number']:<14} | {role:<12} | {status:<9} | {batch:<5} | {gender}")
        
        else:
            print("No members found in this organization.")
            
    except Error as e:
        print("Error searching organization:", e)
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
    