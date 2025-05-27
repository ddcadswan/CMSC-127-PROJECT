import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from database.connection import connect_to_server

class CommitteeGUI:
    def __init__(self, parent, clear_callback=None, button_creator=None):
        self.parent = parent
        self.clear_callback = clear_callback
        self.button_creator = button_creator

        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # --- Committee Form ---
        form_frame = tk.LabelFrame(self.frame, text="Committee Details", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Committee Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Add", command=self.add_committee).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_committee).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_committee).pack(side="left", padx=5)

        # --- Committee List ---
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="Committee ID")
        self.tree.heading("Name", text="Committee Name")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.load_selected_committee)

        # --- Committee Member Section ---
        member_frame = tk.LabelFrame(self.frame, text="Committee Members", padx=10, pady=10)
        member_frame.pack(fill="x", padx=10, pady=5)

        self.member_tree = ttk.Treeview(member_frame,
                                        columns=("MemberID", "OrgID", "Semester", "AY", "Role"),
                                        show="headings")
        self.member_tree.heading("MemberID", text="Membership ID")
        self.member_tree.heading("OrgID", text="Organization ID")
        self.member_tree.heading("Semester", text="Semester")
        self.member_tree.heading("AY", text="Academic Year")
        self.member_tree.heading("Role", text="Role")
        self.member_tree.pack(fill="x", padx=10, pady=5)

        self.refresh_committees()

    def run_query(self, query, params=None, fetch=False):
        conn = connect_to_server("student_org_database")
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            conn.close()
        return []

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
            self.clear_member_tree()
            messagebox.showinfo("Success", "Committee deleted successfully.")

    def load_selected_committee(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item['values'][1])
            self.display_committee_members(item['values'][0])  # load member list

    def display_committee_members(self, committee_id):
        self.clear_member_tree()
        query = """
            SELECT membership_id, organization_id, semester, academic_year, role
            FROM member_committee
            WHERE committee_id = %s
        """
        members = self.run_query(query, (committee_id,), fetch=True)
        for member in members:
            self.member_tree.insert('', tk.END, values=(
                member['membership_id'],
                member['organization_id'],
                member['semester'],
                member['academic_year'],
                member['role']
            ))

    def clear_member_tree(self):
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Committee Management")
    app = CommitteeGUI(root)
    root.mainloop()
