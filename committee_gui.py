import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from database.connection import connect_to_server

class CommitteeGUI:
    def __init__(self, parent, clear_callback=None, button_creator=None):
        self.parent = parent
        self.clear_callback = clear_callback
        self.button_creator = button_creator

        # Create main frame inside the parent
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # Frame for form inputs
        form_frame = tk.LabelFrame(self.frame, text="Committee Details", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Committee Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Add", command=self.add_committee).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_committee).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_committee).pack(side="left", padx=5)

        # Treeview for committee list
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="Committee ID")
        self.tree.heading("Name", text="Committee Name")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.load_selected_committee)

        self.refresh_committees()

        # Frame for committee member management
        member_frame = tk.LabelFrame(self.frame, text="Committee Member Management", padx=10, pady=10)
        member_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(member_frame, text="Membership ID:").grid(row=0, column=0, sticky="w")
        self.member_id_entry = tk.Entry(member_frame, width=20)
        self.member_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(member_frame, text="Org ID:").grid(row=0, column=2, sticky="w")
        self.org_id_entry = tk.Entry(member_frame, width=20)
        self.org_id_entry.grid(row=0, column=3, padx=5)

        tk.Label(member_frame, text="Semester:").grid(row=1, column=0, sticky="w")
        self.semester_entry = tk.Entry(member_frame, width=20)
        self.semester_entry.grid(row=1, column=1, padx=5)

        tk.Label(member_frame, text="Academic Year:").grid(row=1, column=2, sticky="w")
        self.ay_entry = tk.Entry(member_frame, width=20)
        self.ay_entry.grid(row=1, column=3, padx=5)

        tk.Label(member_frame, text="Role:").grid(row=2, column=0, sticky="w")
        self.role_entry = tk.Entry(member_frame, width=20)
        self.role_entry.grid(row=2, column=1, padx=5)

        # Buttons for member management
        tk.Button(member_frame, text="Add Member", command=self.add_member_committee).grid(row=3, column=0, pady=5)
        tk.Button(member_frame, text="Search Member", command=self.search_member_committee).grid(row=3, column=1)
        tk.Button(member_frame, text="Update Role", command=self.update_member_committee).grid(row=3, column=2)
        tk.Button(member_frame, text="Delete Member", command=self.delete_member_committee).grid(row=3, column=3)

        # Treeview to display members in the selected committee
        self.member_tree = ttk.Treeview(self.frame, columns=("MemberID", "OrgID", "Semester", "AY", "Role"), show="headings")
        self.member_tree.heading("MemberID", text="Member ID")
        self.member_tree.heading("OrgID", text="Organization ID")
        self.member_tree.heading("Semester", text="Semester")
        self.member_tree.heading("AY", text="Academic Year")
        self.member_tree.heading("Role", text="Role")
        self.member_tree.pack(fill="x", padx=10, pady=10)


    def run_query(self, query, params=None, fetch=False):
        conn = connect_to_server("student_org_database")
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                return result
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def refresh_committees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        results = self.run_query("SELECT * FROM committee", fetch=True)
        if results:
            for committee in results:
                self.tree.insert('', 'end', values=(committee['committee_id'], committee['committee_name']))

    def add_committee(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a committee name.")
            return
        self.run_query("INSERT INTO committee (committee_name) VALUES (%s)", (name,))
        self.name_entry.delete(0, tk.END)
        self.refresh_committees()
        messagebox.showinfo("Success", "Committee added successfully.")

    def update_committee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a committee to update.")
            return
        item = self.tree.item(selected[0])
        committee_id = item['values'][0]
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Input Error", "Please enter a new name.")
            return
        self.run_query("UPDATE committee SET committee_name = %s WHERE committee_id = %s", (new_name, committee_id))
        self.refresh_committees()
        messagebox.showinfo("Success", "Committee updated successfully.")

    def delete_committee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a committee to delete.")
            return
        item = self.tree.item(selected[0])
        committee_id = item['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this committee?")
        if confirm:
            self.run_query("DELETE FROM committee WHERE committee_id = %s", (committee_id,))
            self.refresh_committees()
            messagebox.showinfo("Success", "Committee deleted successfully.")

    def load_selected_committee(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item['values'][1])

    def add_member_committee(self):
        try:
            values = (
                int(self.member_id_entry.get().strip()),
                int(self.get_selected_committee_id()),
                int(self.org_id_entry.get().strip()),
                self.semester_entry.get().strip(),
                self.ay_entry.get().strip(),
                self.role_entry.get().strip()
            )
        except ValueError:
            messagebox.showwarning("Input Error", "All IDs must be numeric.")
            return

        query = """
            INSERT INTO member_committee
            (membership_id, committee_id, organization_id, semester, academic_year, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.run_query(query, values)
        messagebox.showinfo("Success", "Member added to committee.")

    def get_selected_committee_id(self):
        selected = self.tree.selection()
        if not selected:
            raise ValueError("No committee selected.")
        return self.tree.item(selected[0])['values'][0]


    def update_member_committee(self):
        try:
            values = (
                self.role_entry.get().strip(),
                int(self.member_id_entry.get().strip()),
                int(self.get_selected_committee_id()),
                int(self.org_id_entry.get().strip()),
                self.semester_entry.get().strip(),
                self.ay_entry.get().strip()
            )
        except ValueError:
            messagebox.showwarning("Input Error", "IDs must be numeric.")
            return

        query = """
            UPDATE member_committee
            SET role = %s
            WHERE membership_id = %s AND committee_id = %s AND organization_id = %s 
            AND semester = %s AND academic_year = %s
        """
        self.run_query(query, values)
        messagebox.showinfo("Success", "Role updated.")

    def delete_member_committee(self):
        try:
            values = (
                int(self.member_id_entry.get().strip()),
                int(self.get_selected_committee_id()),
                int(self.org_id_entry.get().strip()),
                self.semester_entry.get().strip(),
                self.ay_entry.get().strip()
            )
        except ValueError:
            messagebox.showwarning("Input Error", "IDs must be numeric.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member record?")
        if confirm:
            query = """
                DELETE FROM member_committee
                WHERE membership_id = %s AND committee_id = %s AND organization_id = %s 
                AND semester = %s AND academic_year = %s
            """
            self.run_query(query, values)
            messagebox.showinfo("Success", "Member removed from committee.")


if __name__ == '__main__':
    root = tk.Tk()
    app = CommitteeGUI(root)
    root.mainloop()
