from tkinter.simpledialog import askstring
import mysql.connector
from database.connection import connect_to_server


import tkinter as tk
from tkinter import messagebox
from functions.operations.reports import (
    view_member_count, view_all_members, view_members_unpaid_fees,
    view_member_orgs, view_member_unpaid_fees, list_active_members,
    view_members_with_unpaid_or_late, view_committee_roles,
    view_total_fee_collected, view_all_students
)
import io
import sys

def capture_output(func, *args):
    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer
    try:
        func(*args)
    finally:
        sys.stdout = sys_stdout
    return buffer.getvalue()

class ReportWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Generate Report")
        self.geometry("600x600")

        title = tk.Label(self, text="Report Options", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        options = [
            "1. View number of members per organization",
            "2. View all members of an organization",
            "3. View members with unpaid or late fees (by semester & year)",
            "4. View organizations of a member (by membership ID)",
            "5. View a member's unpaid fees (by student number)",
            "6. List all active members",
            "7. View members with unpaid or late fees",
            "8. View committee roles per organization",
            "9. View total fee amount collected per organization",
            "10. View all students"
        ]

        for opt in options:
            btn = tk.Button(self, text=opt, width=60, anchor='w', command=lambda o=opt: self.handle_option(o))
            btn.pack(pady=2, padx=10)

        self.output = tk.Text(self, height=15, wrap="word")
        self.output.pack(padx=10, pady=10, fill='both', expand=True)

    def handle_option(self, option_text):
        self.output.delete("1.0", tk.END)
        try:
            if option_text.startswith("1"):
                output = capture_output(view_member_count)
            elif option_text.startswith("2"):

                org_id = askstring("Organization ID", "Enter Organization ID:")
                sort_by = askstring("Sort By", "Choose how to sort:\n1 - role\n2 - status\n3 - gender\n4 - degree program\n5 - batch\n6 - committee")

                if org_id and sort_by:
                    try:
                        from functions.operations.reports import sorted_by
                        query, params = sorted_by(org_id, sort_by)
                        conn = connect_to_server("student_org_database")
                        cursor = conn.cursor()
                        cursor.execute(query, params)
                        results = cursor.fetchall()
                        conn.close()

                        if results:
                            output = f"Members in Organization ID {org_id}:\n" + "\n".join(str(row) for row in results)
                        else:
                            output = "No members found for that organization."
                    except Exception as e:
                        output = f"[Error] {str(e)}"
                else:
                    output = "[Cancelled or Invalid Input]"

            elif option_text.startswith("3"):

                semester = askstring("Semester", "Enter semester (e.g., 2nd):")
                academic_year = askstring("Academic Year", "Enter academic year (e.g., 2024-2025):")

                if semester and academic_year:
                    try:
                        conn = connect_to_server("student_org_database")
                        cursor = conn.cursor()
                        query = """
                            SELECT m.first_name, m.last_name, o.org_name, f.status, f.amount, f.semester, f.academic_year
                            FROM fee f
                            JOIN member m ON f.membership_id = m.membership_id
                            JOIN organization o ON f.organization_id = o.org_id
                            WHERE f.status IN ('unpaid', 'late')
                            AND f.semester = %s
                            AND f.academic_year = %s;
                        """
                        cursor.execute(query, (semester, academic_year))
                        results = cursor.fetchall()
                        conn.close()

                        if results:
                            output = "Members with unpaid/late fees:\n" + "\n".join(str(row) for row in results)
                        else:
                            output = "No records found for those criteria."
                    except Exception as e:
                        output = f"[Error] {str(e)}"
                else:
                    output = "[Cancelled or invalid input]"

            elif option_text.startswith("4"):
                membership_id = askstring("Membership ID", "Enter Membership ID:")
                if membership_id:
                    try:
                        conn = connect_to_server("student_org_database")
                        cursor = conn.cursor()
                        query = """
                            SELECT m.first_name, m.last_name, o.org_name
                            FROM membership ms
                            JOIN member m ON ms.membership_id = m.membership_id
                            JOIN organization o ON ms.organization_id = o.org_id
                            WHERE m.membership_id = %s;
                        """
                        cursor.execute(query, (membership_id,))
                        results = cursor.fetchall()
                        conn.close()

                        if results:
                            output = f"Organizations for member {membership_id}:\n" + "\n".join(str(row) for row in results)
                        else:
                            output = "No organizations found for that member."
                    except Exception as e:
                        output = f"[Error] {str(e)}"
                else:
                    output = "[Cancelled or invalid input]"

            elif option_text.startswith("5"):
                student_number = askstring("Student Number", "Enter Student Number:")
                if student_number:
                    try:
                        conn = connect_to_server("student_org_database")
                        cursor = conn.cursor()
                        query = """
                            SELECT m.first_name, m.last_name, o.org_name, f.fee_name, f.amount, f.status, f.semester, f.academic_year
                            FROM member m
                            JOIN fee f ON m.membership_id = f.membership_id
                            JOIN organization o ON f.organization_id = o.org_id
                            WHERE m.student_number = %s
                            AND f.status IN ('unpaid', 'late');
                        """
                        cursor.execute(query, (student_number,))
                        results = cursor.fetchall()
                        conn.close()

                        if results:
                            output = f"Unpaid/late fees for student {student_number}:\n" + "\n".join(str(row) for row in results)
                        else:
                            output = "No unpaid or late fee records found for that student."
                    except Exception as e:
                        output = f"[Error] {str(e)}"
                else:
                    output = "[Cancelled or invalid input]"

            elif option_text.startswith("6"):
                output = capture_output(list_active_members)
            elif option_text.startswith("7"):
                output = capture_output(view_members_with_unpaid_or_late)
            elif option_text.startswith("8"):
                output = capture_output(view_committee_roles)
            elif option_text.startswith("9"):
                output = capture_output(view_total_fee_collected)
            elif option_text.startswith("10"):
                output = capture_output(view_all_students)
            else:
                output = "[Error] Invalid option selected."
        except Exception as e:
            output = f"[Error] {str(e)}"
        self.output.insert(tk.END, output)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Org Management")
        self.geometry("800x600")

        self.current_frame = None

        title = tk.Label(self, text="Main Menu", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        options = [
            ("Setup Database & Tables", self.mock_action),
            ("Insert Sample Data", self.mock_action),
            ("Add Member", self.mock_action),
            ("Search Options", self.mock_action),
            ("Delete Member", self.mock_action),
            ("Generate Report", self.show_report_ui),
            ("Exit", self.quit)
        ]

        for label, action in options:
            tk.Button(button_frame, text=label, width=30, command=action).pack(pady=3)

        # Main content frame to show reports or input
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mock_action(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Mock action placeholder", font=("Arial", 12)).pack()

    def show_report_ui(self):
        self.clear_content()

        tk.Label(self.content_frame, text="Report Options", font=("Arial", 14, "bold")).pack(pady=5)

        options = [
            ("1. View number of members per organization", lambda: self.run_report(view_member_count)),
            ("2. View all members of an organization", self.report_members_by_org),
            ("3. View members with unpaid or late fees (by semester & year)", self.report_unpaid_by_semester),
            ("4. View organizations of a member (by membership ID)", self.report_member_orgs),
            ("5. View a member's unpaid fees (by student number)", self.report_unpaid_by_student),
            ("6. List all active members", lambda: self.run_report(list_active_members)),
            ("7. View members with unpaid or late fees", lambda: self.run_report(view_members_with_unpaid_or_late)),
            ("8. View committee roles per organization", lambda: self.run_report(view_committee_roles)),
            ("9. View total fee amount collected per organization", lambda: self.run_report(view_total_fee_collected)),
            ("10. View all students", lambda: self.run_report(view_all_students))
        ]


        for label, action in options:
            tk.Button(self.content_frame, text=label, anchor="w", width=60, command=action).pack(pady=2)

        self.output_box = tk.Text(self.content_frame, height=15, wrap="word")
        self.output_box.pack(pady=10, fill="both", expand=True)

    def run_report(self, func):
        self.output_box.delete("1.0", tk.END)
        try:
            result = capture_output(func)
        except Exception as e:
            result = f"[Error] {e}"
        self.output_box.insert(tk.END, result)

    def report_members_by_org(self):
        self.clear_content()
        tk.Label(self.content_frame, text="View Members by Organization", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Organization ID:").pack()
        org_entry = tk.Entry(self.content_frame)
        org_entry.pack()

        tk.Label(self.content_frame, text="Sort By (1=role, 2=status, 3=gender...):").pack()
        sort_entry = tk.Entry(self.content_frame)
        sort_entry.pack()

        def run_custom_query():
            org_id = org_entry.get()
            sort_by = sort_entry.get()
            if org_id and sort_by:
                try:
                    from functions.operations.reports import sorted_by
                    query, params = sorted_by(org_id, sort_by)
                    conn = connect_to_server("student_org_database")
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    conn.close()
                    output = "\n".join(str(row) for row in results) if results else "No members found."
                except Exception as e:
                    output = f"[Error] {e}"
            else:
                output = "[Missing input]"
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output)

        tk.Button(self.content_frame, text="Run Report", command=run_custom_query).pack(pady=5)

        self.output_box = tk.Text(self.content_frame, height=15, wrap="word")
        self.output_box.pack(pady=10, fill="both", expand=True)

    def report_unpaid_by_semester(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Unpaid or Late Fees by Semester", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Semester (e.g., 2nd):").pack()
        semester_entry = tk.Entry(self.content_frame)
        semester_entry.pack()

        tk.Label(self.content_frame, text="Academic Year (e.g., 2024-2025):").pack()
        year_entry = tk.Entry(self.content_frame)
        year_entry.pack()

        def run_query():
            semester = semester_entry.get()
            year = year_entry.get()
            if semester and year:
                try:
                    conn = connect_to_server("student_org_database")
                    cursor = conn.cursor()
                    query = """
                        SELECT m.first_name, m.last_name, o.org_name, f.status, f.amount, f.semester, f.academic_year
                        FROM fee f
                        JOIN member m ON f.membership_id = m.membership_id
                        JOIN organization o ON f.organization_id = o.org_id
                        WHERE f.status IN ('unpaid', 'late')
                        AND f.semester = %s
                        AND f.academic_year = %s;
                    """
                    cursor.execute(query, (semester, year))
                    results = cursor.fetchall()
                    conn.close()
                    output = "\n".join(str(row) for row in results) if results else "No results found."
                except Exception as e:
                    output = f"[Error] {e}"
            else:
                output = "[Missing input]"
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output)

        tk.Button(self.content_frame, text="Run Report", command=run_query).pack(pady=5)

        self.output_box = tk.Text(self.content_frame, height=15, wrap="word")
        self.output_box.pack(pady=10, fill="both", expand=True)


    def report_member_orgs(self):
        self.clear_content()
        tk.Label(self.content_frame, text="View Organizations of a Member", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Membership ID:").pack()
        id_entry = tk.Entry(self.content_frame)
        id_entry.pack()

        def run_query():
            membership_id = id_entry.get()
            if membership_id:
                try:
                    conn = connect_to_server("student_org_database")
                    cursor = conn.cursor()
                    query = """
                        SELECT m.first_name, m.last_name, o.org_name
                        FROM membership ms
                        JOIN member m ON ms.membership_id = m.membership_id
                        JOIN organization o ON ms.organization_id = o.org_id
                        WHERE m.membership_id = %s;
                    """
                    cursor.execute(query, (membership_id,))
                    results = cursor.fetchall()
                    conn.close()
                    output = "\n".join(str(row) for row in results) if results else "No organizations found for that member."
                except Exception as e:
                    output = f"[Error] {e}"
            else:
                output = "[Missing input]"
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output)

        tk.Button(self.content_frame, text="Run Report", command=run_query).pack(pady=5)
        self.output_box = tk.Text(self.content_frame, height=15, wrap="word")
        self.output_box.pack(pady=10, fill="both", expand=True)

    def report_unpaid_by_student(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Unpaid/Late Fees by Student Number", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Student Number:").pack()
        student_entry = tk.Entry(self.content_frame)
        student_entry.pack()

        def run_query():
            student_number = student_entry.get()
            if student_number:
                try:
                    conn = connect_to_server("student_org_database")
                    cursor = conn.cursor()
                    query = """
                        SELECT m.first_name, m.last_name, o.org_name, f.fee_name, f.amount, f.status, f.semester, f.academic_year
                        FROM member m
                        JOIN fee f ON m.membership_id = f.membership_id
                        JOIN organization o ON f.organization_id = o.org_id
                        WHERE m.student_number = %s
                        AND f.status IN ('unpaid', 'late');
                    """
                    cursor.execute(query, (student_number,))
                    results = cursor.fetchall()
                    conn.close()
                    output = "\n".join(str(row) for row in results) if results else "No unpaid/late fees found for that student."
                except Exception as e:
                    output = f"[Error] {e}"
            else:
                output = "[Missing input]"
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output)

        tk.Button(self.content_frame, text="Run Report", command=run_query).pack(pady=5)
        self.output_box = tk.Text(self.content_frame, height=15, wrap="word")
        self.output_box.pack(pady=10, fill="both", expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
