import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from database.connection import connect_to_server
from mysql.connector import Error

class OrganizationManagementGUI:
    def __init__(self, parent_frame, clear_content_callback, create_styled_button_callback):
        self.parent_frame = parent_frame
        self.clear_content = clear_content_callback
        self.create_styled_button = create_styled_button_callback
        
    def show_organization_management(self):
        """Display the main organization management interface"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Organization Management", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Create main container
        main_container = tk.Frame(self.parent_frame, bg='#f0f2f5')
        main_container.pack(fill='both', expand=True, padx=20)
        
        # Create buttons frame
        buttons_frame = tk.Frame(main_container, bg='#f0f2f5')
        buttons_frame.pack(pady=20)
        
        # Organization management buttons
        org_buttons = [
            ("Add Organization", self.show_add_organization, "#27ae60"),
            ("Add Member to Organization", self.show_add_member_to_org, "#3498db"),
            ("Update Organization", self.show_update_organization, "#f39c12"),
            ("Delete Organization", self.show_delete_organization, "#e74c3c"),
            ("Search Organization", self.show_search_organization, "#9b59b6")
        ]
        
        # Create buttons in a grid layout
        for i, (text, command, color) in enumerate(org_buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(buttons_frame, text=text, command=command,
                           font=('Segoe UI', 11, 'bold'), 
                           bg=color, fg='white',
                           width=25, height=2,
                           relief='flat', cursor='hand2')
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Hover effects
            def on_enter(e, btn=btn, color=color):
                btn.configure(bg=self.darken_color(color))
            def on_leave(e, btn=btn, color=color):
                btn.configure(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Configure grid weights
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
    
    def darken_color(self, color):
        """Darken a hex color for hover effects"""
        color_map = {
            "#27ae60": "#229954",
            "#3498db": "#2980b9",
            "#f39c12": "#e67e22",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad"
        }
        return color_map.get(color, color)
    
    def show_add_organization(self):
        """Show add organization form"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Add Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        form_frame.pack(padx=40, pady=20, fill='x')
        
        # Form content
        content_frame = tk.Frame(form_frame, bg='white')
        content_frame.pack(padx=30, pady=30)
        
        # Organization name field
        tk.Label(content_frame, text="Organization Name:", 
                font=('Segoe UI', 12), bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.org_name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), width=40)
        self.org_name_entry.pack(pady=(0, 20))
        self.org_name_entry.focus()
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        # Add button
        add_btn = tk.Button(buttons_frame, text="Add Organization", 
                           command=self.add_organization,
                           font=('Segoe UI', 11, 'bold'), 
                           bg='#27ae60', fg='white', width=15, height=2,
                           relief='flat', cursor='hand2')
        add_btn.pack(side='left', padx=(0, 10))
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="Back", 
                            command=self.show_organization_management,
                            font=('Segoe UI', 11), 
                            bg='#95a5a6', fg='white', width=15, height=2,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left')
    
    def add_organization(self):
        """Add a new organization to the database"""
        org_name = self.org_name_entry.get().strip()
        
        if not org_name:
            messagebox.showerror("Error", "Please enter an organization name.")
            return
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor()
        try:
            query = "INSERT INTO organization (org_name) VALUES (%s)"
            cursor.execute(query, (org_name,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Organization '{org_name}' added successfully with ID: {cursor.lastrowid}")
            self.org_name_entry.delete(0, tk.END)
            
        except Error as e:
            messagebox.showerror("Error", f"Error adding organization: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def show_add_member_to_org(self):
        """Show add member to organization form"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Add Member to Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Main container
        main_container = tk.Frame(self.parent_frame, bg='#f0f2f5')
        main_container.pack(fill='both', expand=True, padx=20)
        
        # Organizations frame
        org_frame = tk.LabelFrame(main_container, text="Select Organization", 
                                 font=('Segoe UI', 12, 'bold'), bg='white', fg='#2c3e50')
        org_frame.pack(fill='x', pady=(0, 20))
        
        # Organizations listbox
        org_list_frame = tk.Frame(org_frame, bg='white')
        org_list_frame.pack(padx=20, pady=15, fill='both')
        
        self.org_listbox = tk.Listbox(org_list_frame, font=('Segoe UI', 10), height=6)
        org_scrollbar = tk.Scrollbar(org_list_frame, orient='vertical', command=self.org_listbox.yview)
        self.org_listbox.configure(yscrollcommand=org_scrollbar.set)
        
        self.org_listbox.pack(side='left', fill='both', expand=True)
        org_scrollbar.pack(side='right', fill='y')
        
        # Load organizations button
        load_orgs_btn = tk.Button(org_frame, text="Load Organizations", 
                                 command=self.load_organizations,
                                 font=('Segoe UI', 10), bg='#3498db', fg='white',
                                 relief='flat', cursor='hand2')
        load_orgs_btn.pack(pady=(0, 15))
        
        # Available members frame
        members_frame = tk.LabelFrame(main_container, text="Available Members", 
                                     font=('Segoe UI', 12, 'bold'), bg='white', fg='#2c3e50')
        members_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Members treeview
        members_tree_frame = tk.Frame(members_frame, bg='white')
        members_tree_frame.pack(padx=20, pady=15, fill='both', expand=True)
        
        # Create treeview for members
        columns = ('ID', 'Name', 'Student Number', 'Degree Program', 'Batch')
        self.members_tree = ttk.Treeview(members_tree_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.members_tree.heading('ID', text='ID')
        self.members_tree.heading('Name', text='Name')
        self.members_tree.heading('Student Number', text='Student Number')
        self.members_tree.heading('Degree Program', text='Degree Program')
        self.members_tree.heading('Batch', text='Batch')
        
        self.members_tree.column('ID', width=50)
        self.members_tree.column('Name', width=200)
        self.members_tree.column('Student Number', width=150)
        self.members_tree.column('Degree Program', width=200)
        self.members_tree.column('Batch', width=80)
        
        # Scrollbar for treeview
        members_scrollbar = ttk.Scrollbar(members_tree_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=members_scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True)
        members_scrollbar.pack(side='right', fill='y')
        
        # Load available members button
        load_members_btn = tk.Button(members_frame, text="Load Available Members", 
                                    command=self.load_available_members,
                                    font=('Segoe UI', 10), bg='#3498db', fg='white',
                                    relief='flat', cursor='hand2')
        load_members_btn.pack(pady=(0, 15))
        
        # Action buttons
        action_frame = tk.Frame(main_container, bg='#f0f2f5')
        action_frame.pack(pady=10)
        
        add_member_btn = tk.Button(action_frame, text="Add Selected Member", 
                                  command=self.add_selected_member_to_org,
                                  font=('Segoe UI', 11, 'bold'), 
                                  bg='#27ae60', fg='white', width=20, height=2,
                                  relief='flat', cursor='hand2')
        add_member_btn.pack(side='left', padx=(0, 10))
        
        back_btn = tk.Button(action_frame, text="Back", 
                            command=self.show_organization_management,
                            font=('Segoe UI', 11), 
                            bg='#95a5a6', fg='white', width=15, height=2,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left')
        
        # Initialize data
        self.load_organizations()
    
    def load_organizations(self):
        """Load organizations into the listbox"""
        self.org_listbox.delete(0, tk.END)
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT org_id, org_name FROM organization ORDER BY org_name")
            organizations = cursor.fetchall()
            
            for org in organizations:
                self.org_listbox.insert(tk.END, f"{org['org_id']} - {org['org_name']}")
                
        except Error as e:
            messagebox.showerror("Error", f"Error loading organizations: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def load_available_members(self):
        """Load available members for the selected organization"""
        selection = self.org_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an organization first.")
            return
        
        # Extract org_id from selection
        selected_text = self.org_listbox.get(selection[0])
        org_id = int(selected_text.split(' - ')[0])
        
        # Clear existing items
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor(dictionary=True)
        try:
            # Get members not in the selected organization
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
            members = cursor.fetchall()
            
            for member in members:
                name = f"{member['first_name']} {member['last_name']}"
                degree = member['degree_program'] or "N/A"
                batch = str(member['batch']) if member['batch'] else "N/A"
                
                self.members_tree.insert('', 'end', values=(
                    member['membership_id'], name, member['student_number'], degree, batch
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Error loading members: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def add_selected_member_to_org(self):
        """Add selected member to selected organization"""
        # Check organization selection
        org_selection = self.org_listbox.curselection()
        if not org_selection:
            messagebox.showwarning("Warning", "Please select an organization.")
            return
        
        # Check member selection
        member_selection = self.members_tree.selection()
        if not member_selection:
            messagebox.showwarning("Warning", "Please select a member.")
            return
        
        # Get selected data
        selected_org_text = self.org_listbox.get(org_selection[0])
        org_id = int(selected_org_text.split(' - ')[0])
        org_name = selected_org_text.split(' - ')[1]
        
        member_data = self.members_tree.item(member_selection[0])['values']
        membership_id = member_data[0]
        member_name = member_data[1]
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor()
        try:
            # Add member to organization
            query = "INSERT INTO membership (membership_id, organization_id) VALUES (%s, %s)"
            cursor.execute(query, (membership_id, org_id))
            conn.commit()
            
            messagebox.showinfo("Success", f"{member_name} has been added to '{org_name}'!")
            
            # Refresh the available members list
            self.load_available_members()
            
        except Error as e:
            messagebox.showerror("Error", f"Error adding member to organization: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def show_update_organization(self):
        """Show update organization form"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Update Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        form_frame.pack(padx=40, pady=20, fill='x')
        
        # Form content
        content_frame = tk.Frame(form_frame, bg='white')
        content_frame.pack(padx=30, pady=30)
        
        # Organization ID field
        tk.Label(content_frame, text="Organization ID:", 
                font=('Segoe UI', 12), bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.update_org_id_entry = tk.Entry(content_frame, font=('Segoe UI', 11), width=40)
        self.update_org_id_entry.pack(pady=(0, 20))
        
        # New organization name field
        tk.Label(content_frame, text="New Organization Name:", 
                font=('Segoe UI', 12), bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.update_org_name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), width=40)
        self.update_org_name_entry.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        # Update button
        update_btn = tk.Button(buttons_frame, text="Update Organization", 
                              command=self.update_organization,
                              font=('Segoe UI', 11, 'bold'), 
                              bg='#f39c12', fg='white', width=18, height=2,
                              relief='flat', cursor='hand2')
        update_btn.pack(side='left', padx=(0, 10))
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="Back", 
                            command=self.show_organization_management,
                            font=('Segoe UI', 11), 
                            bg='#95a5a6', fg='white', width=15, height=2,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left')
    
    def update_organization(self):
        """Update an organization in the database"""
        try:
            org_id = int(self.update_org_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid organization ID (numeric).")
            return
        
        new_org_name = self.update_org_name_entry.get().strip()
        if not new_org_name:
            messagebox.showerror("Error", "Please enter a new organization name.")
            return
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor()
        try:
            # Check if organization exists
            cursor.execute("SELECT org_name FROM organization WHERE org_id = %s", (org_id,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Organization not found.")
                return
            
            old_name = result[0]
            
            # Update organization
            query = "UPDATE organization SET org_name = %s WHERE org_id = %s"
            cursor.execute(query, (new_org_name, org_id))
            conn.commit()
            
            messagebox.showinfo("Success", f"Organization updated successfully!\nOld name: {old_name}\nNew name: {new_org_name}")
            
            # Clear form
            self.update_org_id_entry.delete(0, tk.END)
            self.update_org_name_entry.delete(0, tk.END)
            
        except Error as e:
            messagebox.showerror("Error", f"Error updating organization: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def show_delete_organization(self):
        """Show delete organization form"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Delete Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Warning frame
        warning_frame = tk.Frame(self.parent_frame, bg='#f8d7da', relief='solid', bd=1)
        warning_frame.pack(padx=40, pady=(0, 20), fill='x')
        
        warning_label = tk.Label(warning_frame, text="⚠️ WARNING: This action cannot be undone!", 
                                font=('Segoe UI', 12, 'bold'), 
                                bg='#f8d7da', fg='#721c24')
        warning_label.pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        form_frame.pack(padx=40, pady=20, fill='x')
        
        # Form content
        content_frame = tk.Frame(form_frame, bg='white')
        content_frame.pack(padx=30, pady=30)
        
        # Organization ID field
        tk.Label(content_frame, text="Organization ID to Delete:", 
                font=('Segoe UI', 12), bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.delete_org_id_entry = tk.Entry(content_frame, font=('Segoe UI', 11), width=40)
        self.delete_org_id_entry.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        # Delete button
        delete_btn = tk.Button(buttons_frame, text="Delete Organization", 
                              command=self.delete_organization,
                              font=('Segoe UI', 11, 'bold'), 
                              bg='#e74c3c', fg='white', width=18, height=2,
                              relief='flat', cursor='hand2')
        delete_btn.pack(side='left', padx=(0, 10))
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="Back", 
                            command=self.show_organization_management,
                            font=('Segoe UI', 11), 
                            bg='#95a5a6', fg='white', width=15, height=2,
                            relief='flat', cursor='hand2')
        back_btn.pack(side='left')
    
    def delete_organization(self):
        """Delete an organization from the database"""
        try:
            org_id = int(self.delete_org_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid organization ID (numeric).")
            return
        
        # Confirmation dialog
        result = messagebox.askyesno("Confirm Deletion", 
                                   f"Are you sure you want to delete organization with ID {org_id}?\n\nThis action cannot be undone!")
        
        if not result:
            return
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor()
        try:
            # Check if organization exists and get name
            cursor.execute("SELECT org_name FROM organization WHERE org_id = %s", (org_id,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Organization not found.")
                return
            
            org_name = result[0]
            
            # Delete organization
            query = "DELETE FROM organization WHERE org_id = %s"
            cursor.execute(query, (org_id,))
            conn.commit()
            
            messagebox.showinfo("Success", f"Organization '{org_name}' (ID: {org_id}) deleted successfully.")
            
            # Clear form
            self.delete_org_id_entry.delete(0, tk.END)
            
        except Error as e:
            messagebox.showerror("Error", f"Error deleting organization: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def show_search_organization(self):
        """Show search organization interface"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(self.parent_frame, text="Search Organization", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        search_frame.pack(padx=40, pady=(0, 20), fill='x')
        
        # Search content
        search_content = tk.Frame(search_frame, bg='white')
        search_content.pack(padx=30, pady=20)
        
        # Organization ID field
        tk.Label(search_content, text="Organization ID:", 
                font=('Segoe UI', 12), bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        search_input_frame = tk.Frame(search_content, bg='white')
        search_input_frame.pack(fill='x', pady=(0, 15))
        
        self.search_org_id_entry = tk.Entry(search_input_frame, font=('Segoe UI', 11), width=30)
        self.search_org_id_entry.pack(side='left', padx=(0, 10))
        
        search_btn = tk.Button(search_input_frame, text="Search", 
                              command=self.search_organization,
                              font=('Segoe UI', 10, 'bold'), 
                              bg='#9b59b6', fg='white', width=12,
                              relief='flat', cursor='hand2')
        search_btn.pack(side='left')
        
        # Results frame
        self.results_frame = tk.Frame(self.parent_frame, bg='#f0f2f5')
        self.results_frame.pack(fill='both', expand=True, padx=40, pady=(0, 20))
        
        # Back button
        back_btn = tk.Button(self.parent_frame, text="Back to Organization Management", 
                            command=self.show_organization_management,
                            font=('Segoe UI', 11), 
                            bg='#95a5a6', fg='white', width=25, height=2,
                            relief='flat', cursor='hand2')
        back_btn.pack(pady=10)
    
    def search_organization(self):
        """Search for an organization and display its details and members"""
        try:
            org_id = int(self.search_org_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid organization ID (numeric).")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        conn = connect_to_server("student_org_database")
        if not conn:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = conn.cursor(dictionary=True)
        try:
            # Get organization details
            query = "SELECT * FROM organization WHERE org_id = %s"
            cursor.execute(query, (org_id,))
            org_result = cursor.fetchone()
            
            if not org_result:
                messagebox.showinfo("Not Found", "No organization found with that ID.")
                return
            
            # Organization details frame
            org_details_frame = tk.LabelFrame(self.results_frame, text="Organization Details", 
                                            font=('Segoe UI', 12, 'bold'), bg='white', fg='#2c3e50')
            org_details_frame.pack(fill='x', pady=(0, 20))
            
            details_content = tk.Frame(org_details_frame, bg='white')
            details_content.pack(padx=20, pady=15, fill='x')
            
            # Display organization details
            for key, value in org_result.items():
                detail_frame = tk.Frame(details_content, bg='white')
                detail_frame.pack(fill='x', pady=2)
                
                tk.Label(detail_frame, text=f"{key.replace('_', ' ').title()}:", 
                        font=('Segoe UI', 10, 'bold'), bg='white', fg='#2c3e50',
                        width=20, anchor='w').pack(side='left')
                
                tk.Label(detail_frame, text=str(value), 
                        font=('Segoe UI', 10), bg='white', fg='#34495e',
                        anchor='w').pack(side='left', padx=(10, 0))
            
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
            
            # Members frame
            members_frame = tk.LabelFrame(self.results_frame, 
                                        text=f"Organization Members ({len(members)} total)", 
                                        font=('Segoe UI', 12, 'bold'), bg='white', fg='#2c3e50')
            members_frame.pack(fill='both', expand=True)
            
            if members:
                # Create treeview for members
                members_tree_frame = tk.Frame(members_frame, bg='white')
                members_tree_frame.pack(padx=20, pady=15, fill='both', expand=True)
                
                columns = ('ID', 'Name', 'Student Number', 'Role', 'Status', 'Batch', 'Gender')
                members_tree = ttk.Treeview(members_tree_frame, columns=columns, show='headings', height=10)
                
                # Configure columns
                members_tree.heading('ID', text='ID')
                members_tree.heading('Name', text='Name')
                members_tree.heading('Student Number', text='Student Number')
                members_tree.heading('Role', text='Role')
                members_tree.heading('Status', text='Status')
                members_tree.heading('Batch', text='Batch')
                members_tree.heading('Gender', text='Gender')
                
                members_tree.column('ID', width=50)
                members_tree.column('Name', width=200)
                members_tree.column('Student Number', width=150)
                members_tree.column('Role', width=120)
                members_tree.column('Status', width=100)
                members_tree.column('Batch', width=80)
                members_tree.column('Gender', width=80)
                
                # Add scrollbar
                members_scrollbar = ttk.Scrollbar(members_tree_frame, orient='vertical', command=members_tree.yview)
                members_tree.configure(yscrollcommand=members_scrollbar.set)
                
                members_tree.pack(side='left', fill='both', expand=True)
                members_scrollbar.pack(side='right', fill='y')
                
                # Populate members data
                for member in members:
                    name = f"{member['first_name']} {member['last_name']}"
                    role = member['role'] or "N/A"
                    status = member['status'] or "N/A"
                    batch = str(member['batch']) if member['batch'] else "N/A"
                    gender = member['gender'] or "N/A"
                    
                    members_tree.insert('', 'end', values=(
                        member['membership_id'], name, member['student_number'], 
                        role, status, batch, gender
                    ))
            else:
                no_members_label = tk.Label(members_frame, text="No members found in this organization.", 
                                        font=('Segoe UI', 11), bg='white', fg='#7f8c8d')
                no_members_label.pack(pady=20)
                
        except Error as e:
            messagebox.showerror("Error", f"Error searching organization: {e}")
        finally:
            cursor.close()
            conn.close()