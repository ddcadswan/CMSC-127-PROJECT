import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from database.connection import connect_to_server

class FeesManagementGUI:
    def __init__(self, parent, clear_content_callback, create_styled_button_callback):
        self.parent = parent
        self.clear_content = clear_content_callback
        self.create_styled_button = create_styled_button_callback
        self.content_frame = None
        
    def get_db_connection(self):
        """Establish database connection"""
        return connect_to_server('student_org_database')

    def display_organizations(self):
        """Display all available organizations and return them"""
        connection = self.get_db_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT org_id, org_name FROM organization ORDER BY org_name")
            organizations = cursor.fetchall()
            return organizations
        except Error as err:
            messagebox.showerror("Error", f"Error fetching organizations: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    def get_organization_members(self, org_id):
        """Get all members of a specific organization"""
        connection = self.get_db_connection()
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
            messagebox.showerror("Error", f"Error fetching organization members: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    def show_fees_menu(self):
        """Display the main fees management menu"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Fees Management", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Manage organization fees and payment status", 
                                 font=('Segoe UI', 10), 
                                 bg='white', fg='#7f8c8d')
        subtitle_label.pack(pady=(5, 0))
        
        # Menu options
        options_frame = tk.Frame(self.parent, bg='white')
        options_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        options = [
            ("Add Fee to Organization", "Add a new fee for all members of an organization", 
             self.show_add_fee_form, "#27ae60"),
            ("View Organization Fees", "View and manage fees for a specific organization", 
             self.show_view_fees_form, "#3498db"),
            ("Delete Fee", "Remove a fee from an organization", 
             self.show_delete_fee_form, "#e74c3c"),
            ("Member Fee Status", "View fee status for a specific member", 
             self.show_member_fee_status, "#f39c12"),
            ("Update Payment Status", "Update the payment status of a fee", 
             self.show_update_payment_form, "#9b59b6")
        ]
        
        for title, desc, command, color in options:
            option_frame = tk.Frame(options_frame, bg='#f8f9fa', relief='solid', bd=1)
            option_frame.pack(fill='x', pady=5)
            
            # Option content
            content_frame = tk.Frame(option_frame, bg='#f8f9fa')
            content_frame.pack(fill='x', padx=15, pady=10)
            
            title_label = tk.Label(content_frame, text=title, 
                                  font=('Segoe UI', 11, 'bold'), 
                                  bg='#f8f9fa', fg='#2c3e50')
            title_label.pack(anchor='w')
            
            desc_label = tk.Label(content_frame, text=desc, 
                                 font=('Segoe UI', 9), 
                                 bg='#f8f9fa', fg='#7f8c8d')
            desc_label.pack(anchor='w', pady=(2, 8))
            
            btn = tk.Button(content_frame, text="Select", 
                           font=('Segoe UI', 9, 'bold'),
                           bg=color, fg='white',
                           relief='flat', bd=0,
                           cursor='hand2',
                           command=command)
            btn.pack(anchor='w', ipadx=15, ipady=3)

    def show_add_fee_form(self):
        """Show form to add fee to organization"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Add Fee to Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Organization selection
        org_frame = tk.Frame(self.parent, bg='white')
        org_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        org_label = tk.Label(org_frame, text="Select Organization:", 
                            font=('Segoe UI', 10, 'bold'), 
                            bg='white', fg='#34495e')
        org_label.pack(anchor='w')
        
        # Get organizations
        organizations = self.display_organizations()
        if not organizations:
            messagebox.showerror("Error", "No organizations found")
            return
        
        # Organization dropdown
        self.org_var = tk.StringVar()
        org_dropdown = ttk.Combobox(org_frame, textvariable=self.org_var, 
                                   font=('Segoe UI', 10), state='readonly')
        org_dropdown['values'] = [f"{org[0]} - {org[1]}" for org in organizations]
        org_dropdown.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Fee details form
        form_frame = tk.Frame(self.parent, bg='white')
        form_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        fields = [
            ("Fee Name:", "fee_name"),
            ("Amount (₱):", "amount"),
            ("Due Date (YYYY-MM-DD):", "due_date"),
            ("Semester (e.g., 1st, 2nd):", "semester"),
            ("Academic Year (e.g., 2024-2025):", "academic_year")
        ]
        
        self.fee_entries = {}
        
        for label_text, field_name in fields:
            field_frame = tk.Frame(form_frame, bg='white')
            field_frame.pack(fill='x', pady=8)
            
            label = tk.Label(field_frame, text=label_text, 
                           font=('Segoe UI', 10, 'bold'), 
                           bg='white', fg='#34495e')
            label.pack(anchor='w')
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 10), 
                           relief='solid', bd=1, bg='#f8f9fa')
            entry.pack(fill='x', pady=(5, 0), ipady=5)
            self.fee_entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(self.parent, bg='white')
        button_frame.pack(padx=30, pady=10)
        
        add_btn = tk.Button(button_frame, text="Add Fee to All Members", 
                           font=('Segoe UI', 10, 'bold'),
                           bg="#27ae60", fg='white',
                           relief='flat', bd=0,
                           cursor='hand2',
                           command=self.add_fee_to_organization)
        add_btn.pack(side='left', pady=10, ipady=8, ipadx=20, padx=(0, 10))
        
        back_btn = tk.Button(button_frame, text="Back to Menu", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#95a5a6", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.show_fees_menu)
        back_btn.pack(side='left', pady=10, ipady=8, ipadx=20)

    def add_fee_to_organization(self):
        """Add fee to all members of selected organization"""
        # Get selected organization
        org_selection = self.org_var.get()
        if not org_selection:
            messagebox.showwarning("Input Error", "Please select an organization.")
            return
        
        org_id = int(org_selection.split(' - ')[0])
        
        # Get fee details
        fee_name = self.fee_entries['fee_name'].get().strip()
        amount_str = self.fee_entries['amount'].get().strip()
        due_date = self.fee_entries['due_date'].get().strip()
        semester = self.fee_entries['semester'].get().strip()
        academic_year = self.fee_entries['academic_year'].get().strip()
        
        # Validate inputs
        if not all([fee_name, amount_str, due_date, semester, academic_year]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be positive.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount format.")
            return
        
        # Validate date format
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        
        # Get organization members
        members = self.get_organization_members(org_id)
        if not members:
            messagebox.showwarning("No Members", "No members found in this organization.")
            return
        
        # Confirmation
        result = messagebox.askyesno("Confirm", 
                                   f"This will add the fee '{fee_name}' for {len(members)} members. Continue?")
        if not result:
            return
        
        # Add fees
        connection = self.get_db_connection()
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
            messagebox.showinfo("Success", f"Successfully added fee '{fee_name}' for {fees_added} members.")
            
            # Clear form
            for entry in self.fee_entries.values():
                entry.delete(0, tk.END)
            self.org_var.set('')
            
        except Error as err:
            connection.rollback()
            messagebox.showerror("Error", f"Error adding fees: {err}")
        finally:
            cursor.close()
            connection.close()

    def show_view_fees_form(self):
        """Show form to view organization fees"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="View Organization Fees", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Organization selection
        org_frame = tk.Frame(self.parent, bg='white')
        org_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        org_label = tk.Label(org_frame, text="Select Organization:", 
                            font=('Segoe UI', 10, 'bold'), 
                            bg='white', fg='#34495e')
        org_label.pack(anchor='w')
        
        organizations = self.display_organizations()
        if not organizations:
            messagebox.showerror("Error", "No organizations found")
            return
        
        self.view_org_var = tk.StringVar()
        org_dropdown = ttk.Combobox(org_frame, textvariable=self.view_org_var, 
                                   font=('Segoe UI', 10), state='readonly')
        org_dropdown['values'] = [f"{org[0]} - {org[1]}" for org in organizations]
        org_dropdown.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Button
        btn_frame = tk.Frame(self.parent, bg='white')
        btn_frame.pack(padx=30, pady=10)
        
        view_btn = tk.Button(btn_frame, text="View Fees", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#3498db", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.view_organization_fees)
        view_btn.pack(side='left', pady=10, ipady=8, ipadx=20, padx=(0, 10))
        
        back_btn = tk.Button(btn_frame, text="Back to Menu", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#95a5a6", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.show_fees_menu)
        back_btn.pack(side='left', pady=10, ipady=8, ipadx=20)
        
        # Results area
        results_frame = tk.Frame(self.parent, bg='white')
        results_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        results_label = tk.Label(results_frame, text="Fee Summary:", 
                                font=('Segoe UI', 10, 'bold'), 
                                bg='white', fg='#34495e')
        results_label.pack(anchor='w', pady=(0, 5))
        
        # Create Treeview for better display
        columns = ('Fee Name', 'Academic Year', 'Semester', 'Amount', 'Due Date', 'Total Members', 'Paid', 'Pending')
        self.fees_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        for col in columns:
            self.fees_tree.heading(col, text=col)
            self.fees_tree.column(col, width=100, anchor='center')
        
        # Scrollbar
        fees_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.fees_tree.yview)
        self.fees_tree.configure(yscrollcommand=fees_scrollbar.set)
        
        self.fees_tree.pack(side='left', fill='both', expand=True)
        fees_scrollbar.pack(side='right', fill='y')

    def view_organization_fees(self):
        """View fees for selected organization"""
        org_selection = self.view_org_var.get()
        if not org_selection:
            messagebox.showwarning("Input Error", "Please select an organization.")
            return
        
        org_id = int(org_selection.split(' - ')[0])
        org_name = org_selection.split(' - ')[1]
        
        connection = self.get_db_connection()
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
            
            # Clear previous results
            for item in self.fees_tree.get_children():
                self.fees_tree.delete(item)
            
            if not fee_summary:
                messagebox.showinfo("No Fees", f"No fees found for organization: {org_name}")
                return
            
            # Populate tree
            for fee in fee_summary:
                fee_name, academic_year, semester, amount, due_date, total, paid, pending = fee
                values = (fee_name, academic_year, semester, f"₱{amount:.2f}", 
                         due_date, total, paid, pending)
                self.fees_tree.insert('', 'end', values=values)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching fees: {err}")
        finally:
            cursor.close()
            connection.close()

    def show_delete_fee_form(self):
        """Show form to delete fees"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Delete Fee from Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Warning
        warning_frame = tk.Frame(self.parent, bg='#fff3cd', relief='solid', bd=1)
        warning_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        warning_label = tk.Label(warning_frame, text="⚠️ Warning: This will delete the fee for ALL members in the organization", 
                                font=('Segoe UI', 10, 'bold'), 
                                bg='#fff3cd', fg='#856404')
        warning_label.pack(pady=10)
        
        # Organization selection
        org_frame = tk.Frame(self.parent, bg='white')
        org_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        org_label = tk.Label(org_frame, text="Select Organization:", 
                            font=('Segoe UI', 10, 'bold'), 
                            bg='white', fg='#34495e')
        org_label.pack(anchor='w')
        
        organizations = self.display_organizations()
        if not organizations:
            messagebox.showerror("Error", "No organizations found")
            return
        
        self.delete_org_var = tk.StringVar()
        org_dropdown = ttk.Combobox(org_frame, textvariable=self.delete_org_var, 
                                   font=('Segoe UI', 10), state='readonly')
        org_dropdown['values'] = [f"{org[0]} - {org[1]}" for org in organizations]
        org_dropdown.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Button to load fees
        load_btn_frame = tk.Frame(self.parent, bg='white')
        load_btn_frame.pack(padx=30, pady=10)
        
        load_btn = tk.Button(load_btn_frame, text="Load Fees", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#f39c12", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.load_fees_for_deletion)
        load_btn.pack(side='left', pady=10, ipady=8, ipadx=20, padx=(0, 10))
        
        back_btn = tk.Button(load_btn_frame, text="Back to Menu", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#95a5a6", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.show_fees_menu)
        back_btn.pack(side='left', pady=10, ipady=8, ipadx=20)
        
        # Fees list area
        self.delete_fees_frame = tk.Frame(self.parent, bg='white')
        self.delete_fees_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def load_fees_for_deletion(self):
        """Load fees for selected organization for deletion"""
        org_selection = self.delete_org_var.get()
        if not org_selection:
            messagebox.showwarning("Input Error", "Please select an organization.")
            return
        
        org_id = int(org_selection.split(' - ')[0])
        org_name = org_selection.split(' - ')[1]
        
        # Clear previous content
        for widget in self.delete_fees_frame.winfo_children():
            widget.destroy()
        
        connection = self.get_db_connection()
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
                no_fees_label = tk.Label(self.delete_fees_frame, 
                                        text=f"No fees found for organization: {org_name}", 
                                        font=('Segoe UI', 10), 
                                        bg='white', fg='#7f8c8d')
                no_fees_label.pack(pady=20)
                return
            
            # Display fees
            fees_label = tk.Label(self.delete_fees_frame, text="Select Fee to Delete:", 
                                 font=('Segoe UI', 10, 'bold'), 
                                 bg='white', fg='#34495e')
            fees_label.pack(anchor='w', pady=(0, 10))
            
            self.selected_fee = tk.StringVar()
            
            for i, fee in enumerate(fees):
                fee_name, academic_year, semester, amount, due_date = fee
                fee_text = f"{fee_name} | {academic_year} {semester} | ₱{amount:.2f} | Due: {due_date}"
                
                radio = tk.Radiobutton(self.delete_fees_frame, text=fee_text,
                                      variable=self.selected_fee, value=str(i),
                                      font=('Segoe UI', 9), bg='white')
                radio.pack(anchor='w', pady=2)
            
            # Delete button
            delete_btn = tk.Button(self.delete_fees_frame, text="Delete Selected Fee", 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg="#e74c3c", fg='white',
                                  relief='flat', bd=0,
                                  cursor='hand2',
                                  command=lambda: self.delete_selected_fee(org_id, fees))
            delete_btn.pack(pady=20, ipady=8, ipadx=20)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching fees: {err}")
        finally:
            cursor.close()
            connection.close()

    def delete_selected_fee(self, org_id, fees):
        """Delete the selected fee"""
        selected_index = self.selected_fee.get()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a fee to delete.")
            return
        
        selected_fee = fees[int(selected_index)]
        fee_name, academic_year, semester, amount, due_date = selected_fee
        
        # Confirmation
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete the fee '{fee_name}' "
                                   f"for {academic_year} {semester}?\n\n"
                                   f"This will delete the fee for ALL members in the organization.")
        if not result:
            return
        
        connection = self.get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Delete the fees
            delete_query = """
            DELETE FROM fee 
            WHERE organization_id = %s AND fee_name = %s 
                  AND academic_year = %s AND semester = %s
            """
            
            cursor.execute(delete_query, (org_id, fee_name, academic_year, semester))
            connection.commit()
            
            deleted_count = cursor.rowcount
            messagebox.showinfo("Success", f"Successfully deleted {deleted_count} fee records.")
            
            # Reload fees
            self.load_fees_for_deletion()
            
        except mysql.connector.Error as err:
            connection.rollback()
            messagebox.showerror("Error", f"Error deleting fees: {err}")
        finally:
            cursor.close()
            connection.close()

    def show_member_fee_status(self):
        """Show form to view member fee status"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Member Fee Status", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Student number input
        input_frame = tk.Frame(self.parent, bg='white')
        input_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        input_label = tk.Label(input_frame, text="Enter Student Number:", 
                              font=('Segoe UI', 10, 'bold'), 
                              bg='white', fg='#34495e')
        input_label.pack(anchor='w')
        
        self.student_number_entry = tk.Entry(input_frame, font=('Segoe UI', 10), 
                                           relief='solid', bd=1, bg='#f8f9fa')
        self.student_number_entry.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Button
        btn_frame = tk.Frame(self.parent, bg='white')
        btn_frame.pack(padx=30, pady=10)
        
        search_btn = tk.Button(btn_frame, text="View Fee Status", 
                              font=('Segoe UI', 10, 'bold'),
                              bg="#f39c12", fg='white',
                              relief='flat', bd=0,
                              cursor='hand2',
                              command=self.view_member_fee_status)
        search_btn.pack(side='left', pady=10, ipady=8, ipadx=20, padx=(0, 10))
        
        back_btn = tk.Button(btn_frame, text="Back to Menu", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#95a5a6", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.show_fees_menu)
        back_btn.pack(side='left', pady=10, ipady=8, ipadx=20)
        
        # Results area
        results_frame = tk.Frame(self.parent, bg='white')
        results_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        self.member_results_text = tk.Text(results_frame, height=15, wrap="word", 
                                          font=('Consolas', 9), relief='solid', bd=1,
                                          bg='#f8f9fa', state='disabled')
        
        # Scrollbar for text
        text_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.member_results_text.yview)
        self.member_results_text.configure(yscrollcommand=text_scrollbar.set)
        
        self.member_results_text.pack(side='left', fill='both', expand=True)
        text_scrollbar.pack(side='right', fill='y')

    def view_member_fee_status(self):
        """View fee status for entered student number"""
        student_number = self.student_number_entry.get().strip()
        if not student_number:
            messagebox.showwarning("Input Error", "Please enter a student number.")
            return
        
        connection = self.get_db_connection()
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
            
            # Clear previous results
            self.member_results_text.config(state='normal')
            self.member_results_text.delete(1.0, tk.END)
            
            if not records:
                self.member_results_text.insert(tk.END, "No fee records found for this student number.")
                self.member_results_text.config(state='disabled')
                return
            
            # Display member info
            first_record = records[0]
            result_text = f"Fee Status for {first_record[0]} {first_record[1]}\n"
            result_text += f"Student Number: {first_record[2]}\n"
            result_text += "=" * 80 + "\n\n"
            
            current_org = None
            total_pending = 0
            total_paid = 0
            
            for record in records:
                _, _, _, org_name, fee_name, academic_year, semester, amount, status, due_date, payment_id = record
                
                if org_name != current_org:
                    if current_org is not None:
                        result_text += "-" * 60 + "\n"
                    result_text += f"\nOrganization: {org_name}\n"
                    result_text += "-" * 60 + "\n"
                    current_org = org_name
                
                status_symbol = "✓" if status == 'Paid' else "✗"
                result_text += f"{status_symbol} {fee_name} | {academic_year} {semester} | ₱{amount:.2f} | {status} | Due: {due_date}\n"
                
                if status == 'Paid':
                    total_paid += amount
                else:
                    total_pending += amount
            
            result_text += "\n" + "=" * 80 + "\n"
            result_text += f"Total Paid: ₱{total_paid:.2f}\n"
            result_text += f"Total Pending: ₱{total_pending:.2f}\n"
            result_text += f"Grand Total: ₱{total_paid + total_pending:.2f}\n"
            
            self.member_results_text.insert(tk.END, result_text)
            self.member_results_text.config(state='disabled')
            
        except Error as err:
            messagebox.showerror("Error", f"Error fetching member fee status: {err}")
        finally:
            cursor.close()
            connection.close()

    def show_update_payment_form(self):
        """Show form to update payment status"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.parent, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Update Payment Status", 
                            font=('Segoe UI', 16, 'bold'), 
                            bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Payment number input
        input_frame = tk.Frame(self.parent, bg='white')
        input_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        input_label = tk.Label(input_frame, text="Enter Payment Number:", 
                            font=('Segoe UI', 10, 'bold'), 
                            bg='white', fg='#34495e')
        input_label.pack(anchor='w')
        
        self.payment_number_entry = tk.Entry(input_frame, font=('Segoe UI', 10), 
                                        relief='solid', bd=1, bg='#f8f9fa')
        self.payment_number_entry.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Button to load payment details
        load_btn_frame = tk.Frame(self.parent, bg='white')
        load_btn_frame.pack(padx=30, pady=10)
        
        load_btn = tk.Button(load_btn_frame, text="Load Payment Details", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#3498db", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.load_payment_details)
        load_btn.pack(side='left', pady=10, ipady=8, ipadx=20, padx=(0, 10))
        
        back_btn = tk.Button(load_btn_frame, text="Back to Menu", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#95a5a6", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.show_fees_menu)
        back_btn.pack(side='left', pady=10, ipady=8, ipadx=20)
        
        # Payment details area
        self.payment_details_frame = tk.Frame(self.parent, bg='white')
        self.payment_details_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def load_payment_details(self):
        """Load payment details for the entered payment number"""
        payment_number_str = self.payment_number_entry.get().strip()
        if not payment_number_str:
            messagebox.showwarning("Input Error", "Please enter a payment number.")
            return
        
        try:
            payment_number = int(payment_number_str)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid payment number format.")
            return
        
        # Clear previous content
        for widget in self.payment_details_frame.winfo_children():
            widget.destroy()
        
        connection = self.get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Get current fee details
            query = """
            SELECT f.payment_number, f.fee_name, f.amount, f.status, f.due_date,
                m.first_name, m.last_name, m.student_number, o.org_name,
                f.academic_year, f.semester
            FROM fee f
            JOIN member m ON f.membership_id = m.membership_id
            JOIN organization o ON f.organization_id = o.org_id
            WHERE f.payment_number = %s
            """
            
            cursor.execute(query, (payment_number,))
            fee_info = cursor.fetchone()
            
            if not fee_info:
                no_payment_label = tk.Label(self.payment_details_frame, 
                                        text="Payment number not found.", 
                                        font=('Segoe UI', 10), 
                                        bg='white', fg='#e74c3c')
                no_payment_label.pack(pady=20)
                return
            
            payment_id, fee_name, amount, current_status, due_date, first_name, last_name, student_num, org_name, academic_year, semester = fee_info
            
            # Display payment details
            details_frame = tk.Frame(self.payment_details_frame, bg='#f8f9fa', relief='solid', bd=1)
            details_frame.pack(fill='x', pady=(0, 20))
            
            details_title = tk.Label(details_frame, text="Payment Details", 
                                    font=('Segoe UI', 12, 'bold'), 
                                    bg='#f8f9fa', fg='#2c3e50')
            details_title.pack(pady=(10, 5))
            
            details_info = [
                f"Payment ID: {payment_id}",
                f"Student: {first_name} {last_name} ({student_num})",
                f"Organization: {org_name}",
                f"Fee: {fee_name}",
                f"Academic Year: {academic_year} | Semester: {semester}",
                f"Amount: ₱{amount:.2f}",
                f"Current Status: {current_status}",
                f"Due Date: {due_date}"
            ]
            
            for info in details_info:
                info_label = tk.Label(details_frame, text=info, 
                                    font=('Segoe UI', 9), 
                                    bg='#f8f9fa', fg='#34495e')
                info_label.pack(anchor='w', padx=15, pady=2)
            
            # Status selection
            status_frame = tk.Frame(self.payment_details_frame, bg='white')
            status_frame.pack(fill='x', pady=(0, 20))
            
            status_label = tk.Label(status_frame, text="Select New Status:", 
                                font=('Segoe UI', 10, 'bold'), 
                                bg='white', fg='#34495e')
            status_label.pack(anchor='w', pady=(0, 10))
            
            self.new_status_var = tk.StringVar(value=current_status)
            
            status_options = [
                ("Paid", "#27ae60"),
                ("Pending", "#f39c12"),
                ("Overdue", "#e74c3c")
            ]
            
            for status, color in status_options:
                radio = tk.Radiobutton(status_frame, text=status,
                                    variable=self.new_status_var, value=status,
                                    font=('Segoe UI', 10), bg='white',
                                    fg=color, selectcolor='white')
                radio.pack(anchor='w', pady=2)
            
            # Update button
            update_btn = tk.Button(self.payment_details_frame, text="Update Status", 
                                font=('Segoe UI', 10, 'bold'),
                                bg="#9b59b6", fg='white',
                                relief='flat', bd=0,
                                cursor='hand2',
                                command=lambda: self.update_payment_status(payment_number, current_status))
            update_btn.pack(pady=20, ipady=8, ipadx=20)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching payment details: {err}")
        finally:
            cursor.close()
            connection.close()

    def update_payment_status(self, payment_number, current_status):
        """Update the payment status"""
        new_status = self.new_status_var.get()
        
        if new_status == current_status:
            messagebox.showinfo("No Change", "Status is already set to this value.")
            return
        
        # Confirmation
        result = messagebox.askyesno("Confirm Update", 
                                f"Update payment status from '{current_status}' to '{new_status}'?")
        if not result:
            return
        
        connection = self.get_db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Update the status
            update_query = "UPDATE fee SET status = %s WHERE payment_number = %s"
            cursor.execute(update_query, (new_status, payment_number))
            connection.commit()
            
            messagebox.showinfo("Success", f"Successfully updated payment status from '{current_status}' to '{new_status}'.")
            
            # Clear the form
            self.payment_number_entry.delete(0, tk.END)
            for widget in self.payment_details_frame.winfo_children():
                widget.destroy()
            
        except Error as err:
            connection.rollback()
            messagebox.showerror("Error", f"Error updating fee status: {err}")
        finally:
            cursor.close()
            connection.close()