from functions.operations.reports import * 

# ***********************
# MENU
# ***********************
def print_report_menu():
    while True:
        print("============================================================================")
        print("\t1 - View number of members per organization")
        print("\t2 - View all members of an organization")
        print("\t3 - View members with unpaid or late fees (by semester & academic year)")
        print("\t4 - View organizations of a member (by membership ID)")
        print("\t5 - View a member's unpaid fees (by student number)")
        print("\t6 - List all active members")
        print("\t7 - View members with unpaid or late fees")
        print("\t8 - View committee roles per organization")
        print("\t9 - View total fee amount collected per organization")
        print("\t10 - View all students")
        print("\t0 - Back to Main Menu")
        print

        choice = input("Choose an option: ").strip()
      
        if choice == "1":
           view_member_count()
        elif choice == "2":
            view_all_members()
        elif choice == "3":
            view_members_unpaid_fees()
        elif choice == "4":
            view_member_orgs()
        elif choice == "5":
            view_member_unpaid_fees()
        elif choice == "6":
            list_active_members()
        elif choice == "7":
            view_members_with_unpaid_or_late()
        elif choice == "8":
            view_committee_roles()
        elif choice == "9":
            view_total_fee_collected()
        elif choice == "10":
            view_all_students()
        elif choice == "0":
            print("Back to main menu")
            break
        else:
            print("Invalid option, please try again.")

