from database.setup import setup_database, insert_sample_data
from functions.operations.member_ops import add_member, update_member, delete_member, search_members
from functions.utils.menu import print_report_menu
from functions.operations.fee_ops import *

# ***********************
# MAIN LOOP
# ***********************

def main():
    while True:
        print("\n=== Student Organization Management ===")
        print("99 - Setup Database & Tables")
        print("1 - Insert Sample Data")
        print("2 - Add Member")
        print("3 - Update Member")
        print("4 - Search Options")
        print("5 - Delete Member")
        print("6 - Fees Management")
        print("7 - Generate Report")
        print("0 - Exit")

        choice = input("Choose an option: ").strip()

        if choice == "99":
            setup_database()
        elif choice == "1":
            insert_sample_data()
        elif choice == "2":
            add_member()
        elif choice == "3":
            update_member()
        elif choice == "4":
            search_members()
        elif choice == "5":
            delete_member()
        elif choice == "6":
            fees_menu()
        elif choice == "7":
            print_report_menu()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

