from tkinter.simpledialog import askstring
import mysql.connector

import tkinter as tk
from tkinter import messagebox
from project import (
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
            ("Setup Database & Tables", self.setup_database),
            ("Insert Sample Data", self.insert_sample_data),
            ("Add Member", self.add_member),
            ("Search Options", self.search_options),
            ("Delete Member", self.delete_member),
            ("Generate Report", self.show_report_ui),
            ("Exit", self.quit)
        ]

        for label, action in options:
            tk.Button(button_frame, text=label, width=30, command=action).pack(pady=3)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def setup_database(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Database and tables set up.").pack()

    def insert_sample_data(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Sample data inserted.").pack()

    def add_member(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Add New Member", font=("Arial", 14, "bold")).pack(pady=5)

        labels = ["Student Number", "First Name", "Last Name", "Gender"]
        entries = {}
        for label in labels:
            tk.Label(self.content_frame, text=label).pack()
            entry = tk.Entry(self.content_frame)
            entry.pack()
            entries[label] = entry

        def submit():
            values = [entries[label].get() for label in labels]
            if all(values):
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO member (student_number, first_name, last_name, gender)
                        VALUES (%s, %s, %s, %s);
                    """, tuple(values))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Member added successfully.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")

        tk.Button(self.content_frame, text="Submit", command=submit).pack(pady=10)

    def search_options(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Search Member", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Enter Student Number:").pack()
        search_entry = tk.Entry(self.content_frame)
        search_entry.pack()

        output_box = tk.Text(self.content_frame, height=10, wrap="word")
        output_box.pack(pady=10, fill="both", expand=True)

        def search():
            student_number = search_entry.get()
            if student_number:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM member WHERE student_number = %s", (student_number,))
                    result = cursor.fetchone()
                    conn.close()
                    output_box.delete("1.0", tk.END)
                    if result:
                        output_box.insert(tk.END, str(result))
                    else:
                        output_box.insert(tk.END, "Member not found.")
                except Exception as e:
                    output_box.insert(tk.END, f"[Error] {e}")
            else:
                output_box.insert(tk.END, "[Missing input]")

        tk.Button(self.content_frame, text="Search", command=search).pack(pady=5)

    def delete_member(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Delete Member", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(self.content_frame, text="Enter Student Number to Delete:").pack()
        delete_entry = tk.Entry(self.content_frame)
        delete_entry.pack()

        def delete():
            student_number = delete_entry.get()
            if student_number:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM member WHERE student_number = %s", (student_number,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Deleted", "Member deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Missing Input", "Enter a student number.")

        tk.Button(self.content_frame, text="Delete", command=delete).pack(pady=5)

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
                    from project import sorted_by
                    query, params = sorted_by(org_id, sort_by)
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
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
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
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
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
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
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="student_admin",
                        password="iLove127!",
                        database="student_org_database"
                    )
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
