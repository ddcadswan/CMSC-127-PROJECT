import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys
from database.connection import connect_to_server

def get_db_connection():
    """Establish database connection"""
    return connect_to_server('student_org_database')

def fees_menu():
    """Main fees management menu"""
    while True:
        print("\n====== Fees Management ======")
        print("1. Add Fee to an Organization")
        print("2. View Fees of an Organization")
        print("3. Delete Fee from an Organization")
        print("4. View Member Fee Status")
        print("5. Update Fee Payment Status")
        print("0. Back to Main Menu")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            add_fee_to_organization()
        elif choice == '2':
            view_fees_of_organization()
        elif choice == '3':
            delete_fee_from_organization()
        elif choice == '4':
            view_member_fee_status()
        elif choice == '5':
            update_fee_payment_status()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")

def display_organizations():
    """Display all available organizations"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT org_id, org_name FROM organization ORDER BY org_name")
        organizations = cursor.fetchall()
        
        if organizations:
            print("\nAvailable Organizations:")
            print("-" * 40)
            for org_id, org_name in organizations:
                print(f"{org_id}. {org_name}")
            print("-" * 40)
        else:
            print("No organizations found.")
        
        return organizations
    except Error as err:
        print(f"Error fetching organizations: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_organization_members(org_id):
    """Get all members of a specific organization"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT m.membership_id, m.first_name, m.last_name, m.student_number
        FROM member m
        JOIN membership ms ON m.membership_id = ms.membership_id
        WHERE ms.organization_id = %s
        ORDER BY m.last_name, m.first_name
        """
        cursor.execute(query, (org_id,))
        members = cursor.fetchall()
        return members
    except mysql.connector.Error as err:
        print(f"Error fetching organization members: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def add_fee_to_organization():
    """Add a fee that applies to all members of an organization"""
    organizations = display_organizations()
    if not organizations:
        return
    
    try:
        org_id = int(input("\nEnter organization ID: "))
        
        # Verify organization exists
        org_exists = any(org[0] == org_id for org in organizations)
        if not org_exists:
            print("Invalid organization ID.")
            return
        
        # Get fee details
        fee_name = input("Enter fee name: ").strip()
        if not fee_name:
            print("Fee name cannot be empty.")
            return
        
        amount = float(input("Enter fee amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        
        semester = input("Enter semester (e.g.,1st, 2nd): ").strip()
        academic_year = input("Enter academic year (e.g., 2024-2025): ").strip()
        
        # Get organization members
        members = get_organization_members(org_id)
        if not members:
            print("No members found in this organization.")
            return
        
        print(f"\nThis will add the fee '{fee_name}' for {len(members)} members.")
        confirm = input("Continue? (y/n): ").lower()
        
        if confirm != 'y':
            print("Operation cancelled.")
            return
        
        # Add fee for each member
        connection = get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO fee (status, amount, due_date, semester, fee_name, 
                           academic_year, membership_id, organization_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            fees_added = 0
            for member in members:
                membership_id = member[0]
                values = ('Pending', amount, due_date, semester, fee_name, 
                         academic_year, membership_id, org_id)
                cursor.execute(insert_query, values)
                fees_added += 1
            
            connection.commit()
            print(f"\nSuccessfully added fee '{fee_name}' for {fees_added} members.")
            
        except Error as err:
            connection.rollback()
            print(f"Error adding fees: {err}")
        finally:
            cursor.close()
            connection.close()
            
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_fees_of_organization():
    """View all fees for a specific organization"""
    organizations = display_organizations()
    if not organizations:
        return
    
    try:
        org_id = int(input("\nEnter organization ID: "))
        
        # Verify organization exists
        org_name = None
        for org in organizations:
            if org[0] == org_id:
                org_name = org[1]
                break
        
        if not org_name:
            print("Invalid organization ID.")
            return
        
        connection = get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Get fee summary
            summary_query = """
            SELECT fee_name, academic_year, semester, amount, due_date,
                   COUNT(*) as total_members,
                   SUM(CASE WHEN status = 'Paid' THEN 1 ELSE 0 END) as paid_count,
                   SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_count
            FROM fee 
            WHERE organization_id = %s
            GROUP BY fee_name, academic_year, semester, amount, due_date
            ORDER BY academic_year DESC, semester, due_date
            """
            
            cursor.execute(summary_query, (org_id,))
            fee_summary = cursor.fetchall()
            
            if not fee_summary:
                print(f"\nNo fees found for organization: {org_name}")
                return
            
            print(f"\n--- Fee Summary for {org_name} ---")
            print("=" * 80)
            
            for fee in fee_summary:
                fee_name, academic_year, semester, amount, due_date, total, paid, pending = fee
                print(f"\nFee: {fee_name}")
                print(f"Academic Year: {academic_year} | Semester: {semester}")
                print(f"Amount: P{amount:.2f} | Due Date: {due_date}")
                print(f"Status: {paid}/{total} paid, {pending} pending")
                print("-" * 60)
            
            # Option to view detailed member-wise breakdown
            print("\nOptions:")
            print("1. View detailed member breakdown for a specific fee")
            print("2. Return to fees menu")
            
            choice = input("Enter choice: ")
            if choice == '1':
                view_detailed_fee_breakdown(org_id, org_name)
                
        except mysql.connector.Error as err:
            print(f"Error fetching fees: {err}")
        finally:
            cursor.close()
            connection.close()
            
    except ValueError:
        print("Invalid input. Please enter a valid organization ID.")

def view_detailed_fee_breakdown(org_id, org_name):
    """View detailed member-wise fee breakdown"""
    fee_name = input("Enter fee name to view details: ").strip()
    academic_year = input("Enter academic year: ").strip()
    semester = input("Enter semester: ").strip()
    
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        detail_query = """
        SELECT f.payment_number, m.first_name, m.last_name, m.student_number,
               f.status, f.amount, f.due_date
        FROM fee f
        JOIN member m ON f.membership_id = m.membership_id
        WHERE f.organization_id = %s AND f.fee_name = %s 
              AND f.academic_year = %s AND f.semester = %s
        ORDER BY m.last_name, m.first_name
        """
        
        cursor.execute(detail_query, (org_id, fee_name, academic_year, semester))
        details = cursor.fetchall()
        
        if not details:
            print("No matching fee records found.")
            return
        
        print(f"\n--- Detailed Breakdown: {fee_name} ---")
        print(f"Organization: {org_name}")
        print(f"Academic Year: {academic_year} | Semester: {semester}")
        print("=" * 80)
        print(f"{'ID':<6} {'Name':<25} {'Student #':<12} {'Status':<10} {'Amount':<10}")
        print("-" * 80)
        
        for record in details:
            payment_id, first_name, last_name, student_num, status, amount, due_date = record
            full_name = f"{first_name} {last_name}"
            print(f"{payment_id:<6} {full_name:<25} {student_num:<12} {status:<10} P{amount:<9.2f}")
        
    except mysql.connector.Error as err:
        print(f"Error fetching fee details: {err}")
    finally:
        cursor.close()
        connection.close()

def delete_fee_from_organization():
    """Delete a specific fee from an organization"""
    organizations = display_organizations()
    if not organizations:
        return
    
    try:
        org_id = int(input("\nEnter organization ID: "))
        
        # Verify organization exists
        org_name = None
        for org in organizations:
            if org[0] == org_id:
                org_name = org[1]
                break
        
        if not org_name:
            print("Invalid organization ID.")
            return
        
        # Show existing fees for this organization
        connection = get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Get unique fees for this organization
            fees_query = """
            SELECT DISTINCT fee_name, academic_year, semester, amount, due_date
            FROM fee 
            WHERE organization_id = %s
            ORDER BY academic_year DESC, semester, fee_name
            """
            
            cursor.execute(fees_query, (org_id,))
            fees = cursor.fetchall()
            
            if not fees:
                print(f"No fees found for organization: {org_name}")
                return
            
            print(f"\nExisting fees for {org_name}:")
            print("-" * 60)
            for i, fee in enumerate(fees, 1):
                fee_name, academic_year, semester, amount, due_date = fee
                print(f"{i}. {fee_name} | {academic_year} {semester} | P{amount:.2f} | Due: {due_date}")
            print("-" * 60)
            
            choice = int(input("Enter fee number to delete (0 to cancel): "))
            
            if choice == 0:
                print("Operation cancelled.")
                return
            
            if choice < 1 or choice > len(fees):
                print("Invalid fee selection.")
                return
            
            selected_fee = fees[choice - 1]
            fee_name, academic_year, semester, amount, due_date = selected_fee
            
            # Count affected records
            count_query = """
            SELECT COUNT(*) FROM fee 
            WHERE organization_id = %s AND fee_name = %s 
                  AND academic_year = %s AND semester = %s
            """
            cursor.execute(count_query, (org_id, fee_name, academic_year, semester))
            count = cursor.fetchone()[0]
            
            print(f"\nThis will delete {count} fee records for '{fee_name}'.")
            print(f"Academic Year: {academic_year} | Semester: {semester}")
            confirm = input("Are you sure? (y/n): ").lower()
            
            if confirm != 'y':
                print("Operation cancelled.")
                return
            
            # Delete the fees
            delete_query = """
            DELETE FROM fee 
            WHERE organization_id = %s AND fee_name = %s 
                  AND academic_year = %s AND semester = %s
            """
            
            cursor.execute(delete_query, (org_id, fee_name, academic_year, semester))
            connection.commit()
            
            deleted_count = cursor.rowcount
            print(f"\nSuccessfully deleted {deleted_count} fee records.")
            
        except mysql.connector.Error as err:
            connection.rollback()
            print(f"Error deleting fees: {err}")
        finally:
            cursor.close()
            connection.close()
            
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_member_fee_status():
    """View fee status for a specific member"""
    try:
        student_number = input("Enter student number: ").strip()
        
        connection = get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Get member info and fees
            query = """
            SELECT m.first_name, m.last_name, m.student_number,
                   o.org_name, f.fee_name, f.academic_year, f.semester,
                   f.amount, f.status, f.due_date, f.payment_number
            FROM member m
            JOIN fee f ON m.membership_id = f.membership_id
            JOIN organization o ON f.organization_id = o.org_id
            WHERE m.student_number = %s
            ORDER BY f.academic_year DESC, f.semester, o.org_name, f.fee_name
            """
            
            cursor.execute(query, (student_number,))
            records = cursor.fetchall()
            
            if not records:
                print("No fee records found for this student number.")
                return
            
            # Display member info
            first_record = records[0]
            print(f"\n--- Fee Status for {first_record[0]} {first_record[1]} ---")
            print(f"Student Number: {first_record[2]}")
            print("=" * 80)
            
            current_org = None
            total_pending = 0
            total_paid = 0
            
            for record in records:
                _, _, _, org_name, fee_name, academic_year, semester, amount, status, due_date, payment_id = record
                
                if org_name != current_org:
                    if current_org is not None:
                        print("-" * 60)
                    print(f"\nOrganization: {org_name}")
                    print("-" * 60)
                    current_org = org_name
                
                status_symbol = "✓" if status == 'Paid' else "✗"
                print(f"{status_symbol} {fee_name} | {academic_year} {semester} | P{amount:.2f} | {status} | Due: {due_date}")
                
                if status == 'Paid':
                    total_paid += amount
                else:
                    total_pending += amount
            
            print("=" * 80)
            print(f"Total Paid: P{total_paid:.2f}")
            print(f"Total Pending: P{total_pending:.2f}")
            print(f"Grand Total: P{total_paid + total_pending:.2f}")
            
        except Error as err:
            print(f"Error fetching member fee status: {err}")
        finally:
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"An error occurred: {e}")

def update_fee_payment_status():
    """Update payment status of a fee"""
    try:
        payment_number = int(input("Enter payment number: "))
        
        connection = get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Get current fee details
            query = """
            SELECT f.payment_number, f.fee_name, f.amount, f.status, f.due_date,
                   m.first_name, m.last_name, m.student_number, o.org_name
            FROM fee f
            JOIN member m ON f.membership_id = m.membership_id
            JOIN organization o ON f.organization_id = o.org_id
            WHERE f.payment_number = %s
            """
            
            cursor.execute(query, (payment_number,))
            fee_info = cursor.fetchone()
            
            if not fee_info:
                print("Payment number not found.")
                return
            
            payment_id, fee_name, amount, current_status, due_date, first_name, last_name, student_num, org_name = fee_info
            
            print(f"\n--- Fee Details ---")
            print(f"Payment ID: {payment_id}")
            print(f"Student: {first_name} {last_name} ({student_num})")
            print(f"Organization: {org_name}")
            print(f"Fee: {fee_name}")
            print(f"Amount: P{amount:.2f}")
            print(f"Current Status: {current_status}")
            print(f"Due Date: {due_date}")
            
            print(f"\nStatus Options:")
            print("1. Paid")
            print("2. Pending")
            print("3. Overdue")
            print("0. Cancel")
            
            choice = input("Select new status: ")
            
            status_map = {
                '1': 'Paid',
                '2': 'Pending',
                '3': 'Overdue'
            }
            
            if choice == '0':
                print("Operation cancelled.")
                return
            
            if choice not in status_map:
                print("Invalid choice.")
                return
            
            new_status = status_map[choice]
            
            if new_status == current_status:
                print("Status is already set to this value.")
                return
            
            # Update the status
            update_query = "UPDATE fee SET status = %s WHERE payment_number = %s"
            cursor.execute(update_query, (new_status, payment_number))
            connection.commit()
            
            print(f"\nSuccessfully updated payment status from '{current_status}' to '{new_status}'.")
            
        except Error as err:
            connection.rollback()
            print(f"Error updating fee status: {err}")
        finally:
            cursor.close()
            connection.close()
            
    except ValueError:
        print("Invalid payment number. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Test the fee management system
    print("Fee Management System")
    fees_menu()