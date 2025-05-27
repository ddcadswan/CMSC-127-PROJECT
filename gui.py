from tkinter.simpledialog import askstring
import mysql.connector
from database.connection import connect_to_server

import tkinter as tk
from tkinter import messagebox, ttk
from functions.operations.reports import (
    view_member_count, view_all_members, view_members_unpaid_fees,
    view_member_orgs, view_member_unpaid_fees, list_active_members,
    view_members_with_unpaid_or_late, view_committee_roles,
    view_total_fee_collected, view_all_students
)
from functions.operations.member_ops import update_member
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
        self.title("Student Organization Management System")
        self.geometry("1000x700")
        self.configure(bg='#f0f2f5')
        
        # Configure style
        self.setup_styles()
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()

    def setup_styles(self):
        """Configure modern styling for the application"""
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom button style
        style.configure('Modern.TButton',
                       background='#4a90e2',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', '#357abd'),
                           ('pressed', '#2968a3')])
        
        # Header button style
        style.configure('Header.TButton',
                       background='#2c3e50',
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Header.TButton',
                 background=[('active', '#34495e'),
                           ('pressed', '#1a252f')])

    def create_header(self):
        """Create modern header with gradient-like appearance"""
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(expand=True, fill='both')
        
        # Icon placeholder 
        icon_label = tk.Label(title_frame, font=('Arial', 24), 
                             bg='#2c3e50', fg='#ecf0f1')
        icon_label.pack(side='left', padx=(20, 10), pady=15)
        
        # Title text
        title_label = tk.Label(title_frame, text="Student Organization Management System", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(side='left', pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Manage members, organizations, and reports", 
                                 font=('Segoe UI', 10), 
                                 bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(side='left', padx=(10, 0), pady=(25, 0))

    def create_main_content(self):
        """Create the main content area with navigation and content panels"""
        main_container = tk.Frame(self, bg='#f0f2f5')
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Navigation panel
        self.create_navigation_panel(main_container)
        
        # Content panel
        self.create_content_panel(main_container)

    def create_navigation_panel(self, parent):
        """Create modern navigation sidebar"""
        nav_frame = tk.Frame(parent, bg='white', width=280, relief='solid', bd=1)
        nav_frame.pack(side='left', fill='y', padx=(0, 20))
        nav_frame.pack_propagate(False)
        
        # Navigation title
        nav_title = tk.Label(nav_frame, text="Main Menu", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg='white', fg='#2c3e50')
        nav_title.pack(pady=(20, 15), padx=20)
        
        # Navigation buttons
        nav_options = [
            (" Setup Database & Tables", self.setup_database, "#e74c3c"),
            (" Insert Sample Data", self.insert_sample_data, "#f39c12"),
            (" Add Member", self.add_member, "#27ae60"),
            (" Update Member", self.update_member, "#17a2b8"),
            (" Search Options", self.search_options, "#3498db"),
            (" Delete Member", self.delete_member, "#e67e22"),
            (" Generate Report", self.show_report_ui, "#9b59b6"),
            (" Exit", self.quit, "#95a5a6")
        ]
        
        for text, command, color in nav_options:
            btn_frame = tk.Frame(nav_frame, bg='white')
            btn_frame.pack(fill='x', padx=15, pady=3)
            
            btn = tk.Button(btn_frame, text=text, 
                           font=('Segoe UI', 10),
                           bg=color, fg='white',
                           relief='flat', bd=0,
                           cursor='hand2',
                           anchor='w',
                           command=command)
            btn.pack(fill='x', ipady=8)
            
            # Hover effects
            def on_enter(e, button=btn, original_color=color):
                button.configure(bg=self.darken_color(original_color))
            
            def on_leave(e, button=btn, original_color=color):
                button.configure(bg=original_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#e74c3c": "#c0392b",
            "#f39c12": "#d68910",
            "#27ae60": "#229954",
            "#3498db": "#2980b9",
            "#e67e22": "#d35400",
            "#9b59b6": "#8e44ad",
            "#95a5a6": "#7f8c8d"
        }
        return color_map.get(color, color)

    def create_content_panel(self, parent):
        """Create main content display area"""
        content_container = tk.Frame(parent, bg='#f0f2f5')
        content_container.pack(side='right', fill='both', expand=True)
        
        # Welcome panel
        self.content_frame = tk.Frame(content_container, bg='white', relief='solid', bd=1)
        self.content_frame.pack(fill='both', expand=True)
        
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Display welcome screen with system overview"""
        self.clear_content()
        
        # Welcome header
        welcome_frame = tk.Frame(self.content_frame, bg='white')
        welcome_frame.pack(fill='x', padx=30, pady=30)
        
        welcome_title = tk.Label(welcome_frame, text="Welcome to Student Organization Management", 
                                font=('Segoe UI', 16, 'bold'), 
                                bg='white', fg='#2c3e50')
        welcome_title.pack()
        
        welcome_subtitle = tk.Label(welcome_frame, text="Select an option from the menu to get started", 
                                   font=('Segoe UI', 11), 
                                   bg='white', fg='#7f8c8d')
        welcome_subtitle.pack(pady=(5, 0))
        
        # Feature cards
        cards_frame = tk.Frame(self.content_frame, bg='white')
        cards_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        features = [
            (" Member Management", "Add, search, and manage student members"),
            (" Organization Tracking", "Track member organizations and roles"),
            (" Fee Management", "Monitor payment status and generate reports"),
            (" Comprehensive Reports", "Generate detailed analytics and reports")
        ]
        
        for i, (title, desc) in enumerate(features):
            row = i // 2
            col = i % 2
            
            card = tk.Frame(cards_frame, bg='#f8f9fa', relief='solid', bd=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew', ipadx=20, ipady=15)
            
            card_title = tk.Label(card, text=title, 
                                 font=('Segoe UI', 12, 'bold'), 
                                 bg='#f8f9fa', fg='#2c3e50')
            card_title.pack()
            
            card_desc = tk.Label(card, text=desc, 
                                font=('Segoe UI', 9), 
                                bg='#f8f9fa', fg='#7f8c8d',
                                wraplength=200)
            card_desc.pack(pady=(5, 0))
        
        # Configure grid weights
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_form_section(self, title, fields):
        """Create a styled form section"""
        # Header
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text=title, 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Form container
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        entries = {}
        for field in fields:
            field_frame = tk.Frame(form_frame, bg='white')
            field_frame.pack(fill='x', pady=8)
            
            label = tk.Label(field_frame, text=field, 
                           font=('Segoe UI', 10, 'bold'), 
                           bg='white', fg='#34495e')
            label.pack(anchor='w')
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 10), 
                           relief='solid', bd=1, bg='#f8f9fa')
            entry.pack(fill='x', pady=(5, 0), ipady=5)
            entries[field] = entry
        
        return entries

    def create_styled_button(self, parent, text, command, color="#4a90e2"):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, 
                       font=('Segoe UI', 10, 'bold'),
                       bg=color, fg='white',
                       relief='flat', bd=0,
                       cursor='hand2',
                       command=command)
        btn.pack(pady=10, ipady=8, ipadx=20)
        return btn

    def setup_database(self):
        self.clear_content()
        
        # Status display
        status_frame = tk.Frame(self.content_frame, bg='white')
        status_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Success message
        icon_label = tk.Label(status_frame, font=('Arial', 48), bg='white')
        icon_label.pack(pady=(50, 20))
        
        title_label = tk.Label(status_frame, text="Database Setup Complete", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#27ae60')
        title_label.pack()
        
        desc_label = tk.Label(status_frame, text="Database and tables have been set up successfully.", 
                             font=('Segoe UI', 11), 
                             bg='white', fg='#7f8c8d')
        desc_label.pack(pady=(10, 0))

    def insert_sample_data(self):
        self.clear_content()
        
        # Status display
        status_frame = tk.Frame(self.content_frame, bg='white')
        status_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Success message
        icon_label = tk.Label(status_frame, font=('Arial', 48), bg='white')
        icon_label.pack(pady=(50, 20))
        
        title_label = tk.Label(status_frame, text="Sample Data Inserted", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#f39c12')
        title_label.pack()
        
        desc_label = tk.Label(status_frame, text="Sample data has been inserted successfully.", 
                             font=('Segoe UI', 11), 
                             bg='white', fg='#7f8c8d')
        desc_label.pack(pady=(10, 0))

    def add_member(self):
        self.clear_content()
        
        labels = ["Student Number", "First Name", "Last Name", "Gender", "Batch(year)", "Degree Program", "Status(active/inactive)", "Role"]
        entries = self.create_form_section("Add New Member", labels)

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
                        INSERT INTO member (student_number, first_name, last_name, gender, batch, degree_program, status, role)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, tuple(values))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Member added successfully.")
                    # Clear form
                    for entry in entries.values():
                        entry.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Add Member", submit, "#27ae60")

    def update_member(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Update Member", 
                            font=('Segoe UI', 16, 'bold'), 
                            bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Search section
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        search_label = tk.Label(search_frame, text="Find Member to Update:", 
                            font=('Segoe UI', 12, 'bold'), 
                            bg='white', fg='#34495e')
        search_label.pack(anchor='w', pady=(0, 10))
        
        # Search options
        search_option_frame = tk.Frame(search_frame, bg='white')
        search_option_frame.pack(fill='x', pady=(0, 10))
        
        self.search_var = tk.StringVar(value="student_number")
        
        radio1 = tk.Radiobutton(search_option_frame, text="By Student Number", 
                            variable=self.search_var, value="student_number",
                            bg='white', font=('Segoe UI', 10))
        radio1.pack(side='left', padx=(0, 20))
        
        radio2 = tk.Radiobutton(search_option_frame, text="By Membership ID", 
                            variable=self.search_var, value="membership_id",
                            bg='white', font=('Segoe UI', 10))
        radio2.pack(side='left')
        
        # Search input
        search_input_label = tk.Label(search_frame, text="Enter Value:", 
                                    font=('Segoe UI', 10, 'bold'), 
                                    bg='white', fg='#34495e')
        search_input_label.pack(anchor='w')
        
        self.search_entry = tk.Entry(search_frame, font=('Segoe UI', 10), 
                                    relief='solid', bd=1, bg='#f8f9fa')
        self.search_entry.pack(fill='x', pady=(5, 10), ipady=5)
        
        # Search button
        search_btn_frame = tk.Frame(search_frame, bg='white')
        search_btn_frame.pack()
        self.create_styled_button(search_btn_frame, "Find Member", self.find_member_for_update, "#17a2b8")
        
        # Update form (initially hidden)
        self.update_form_frame = tk.Frame(self.content_frame, bg='white')
        self.update_form_frame.pack(fill='both', expand=True, padx=30, pady=(20, 30))
        
    def find_member_for_update(self):
        search_value = self.search_entry.get().strip()
        search_type = self.search_var.get()
        
        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a value to search.")
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="student_admin",
                password="iLove127!",
                database="student_org_database"
            )
            cursor = conn.cursor(dictionary=True)
            
            if search_type == "membership_id":
                cursor.execute("SELECT * FROM member WHERE membership_id = %s", (search_value,))
            else:
                cursor.execute("SELECT * FROM member WHERE student_number = %s", (search_value,))
            
            member = cursor.fetchone()
            conn.close()
            
            if member:
                self.show_update_form(member)
            else:
                messagebox.showinfo("Not Found", "No member found with the given information.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")


    def show_update_form(self, member):
        # Clear existing form
        for widget in self.update_form_frame.winfo_children():
            widget.destroy()
        
        # Form header
        form_header = tk.Label(self.update_form_frame, text="Update Member Information", 
                            font=('Segoe UI', 14, 'bold'), 
                            bg='white', fg='#2c3e50')
        form_header.pack(pady=(0, 15))
        
        # Create main container for centering
        main_container = tk.Frame(self.update_form_frame, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # Create scrollable area
        # Canvas and scrollbar setup
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        # Create a centered container within the scrollable frame
        centered_container = tk.Frame(scrollable_frame, bg='white')
        centered_container.pack(expand=True, fill='both')
        
        # Content frame - this will be centered
        content_frame = tk.Frame(centered_container, bg='white')
        content_frame.pack(expand=True, pady=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window with proper centering
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Function to center content when canvas size changes
        def center_content(event=None):
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:  # Make sure canvas is initialized
                # Update the window to center it
                canvas.delete("content_window")
                canvas.create_window((canvas_width//2, 0), window=scrollable_frame, anchor="n", tags="content_window")
        
        # Bind to canvas resize event
        canvas.bind('<Configure>', center_content)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Current info display (inside content frame)
        current_info_frame = tk.Frame(content_frame, bg='#e8f5e8', relief='solid', bd=1)
        current_info_frame.pack(pady=(0, 20), padx=20)
        
        current_label = tk.Label(current_info_frame, text="Current Information:", 
                                font=('Segoe UI', 11, 'bold'), 
                                bg='#e8f5e8', fg='#2c3e50')
        current_label.pack(pady=(10, 5))
        
        current_text = f"Name: {member['first_name']} {member['last_name']}\n"
        current_text += f"Student Number: {member['student_number']}\n"
        current_text += f"Status: {member['status']}\n"
        current_text += f"Role: {member['role']}"
        
        current_info_label = tk.Label(current_info_frame, text=current_text, 
                                    font=('Segoe UI', 9), 
                                    bg='#e8f5e8', fg='#34495e')
        current_info_label.pack(pady=(0, 10))
        
        # Update form fields (inside content frame)
        form_fields_frame = tk.Frame(content_frame, bg='white')
        form_fields_frame.pack(padx=20)
        
        fields = ['first_name', 'last_name', 'student_number', 'gender', 'batch', 'degree_program', 'status', 'role']
        field_labels = ['First Name', 'Last Name', 'Student Number', 'Gender', 'Batch (Year)', 'Degree Program', 'Status', 'Role']
        
        self.update_entries = {}
        
        for field, label in zip(fields, field_labels):
            field_frame = tk.Frame(form_fields_frame, bg='white')
            field_frame.pack(fill='x', pady=8)
            
            # Label with current value
            current_value = str(member[field]) if member[field] is not None else ""
            label_text = f"{label} (Current: {current_value}):"
            
            field_label = tk.Label(field_frame, text=label_text, 
                                font=('Segoe UI', 9, 'bold'), 
                                bg='white', fg='#34495e')
            field_label.pack(anchor='w')
            
            # Entry field with placeholder
            entry = tk.Entry(field_frame, font=('Segoe UI', 10), 
                            relief='solid', bd=1, bg='#f8f9fa')
            entry.pack(fill='x', pady=(5, 0), ipady=5)
            entry.insert(0, current_value)  # Pre-fill with current value
            
            self.update_entries[field] = entry
        
        # Store member info for update
        self.current_member = member
        
        # Update button (inside content frame)
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(pady=30)
        
        update_btn = tk.Button(button_frame, text="Update Member", 
                            font=('Segoe UI', 10, 'bold'),
                            bg="#17a2b8", fg='white',
                            relief='flat', bd=0,
                            cursor='hand2',
                            command=self.perform_update)
        update_btn.pack(pady=10, ipady=8, ipadx=20)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Initial centering after a short delay to ensure canvas is ready
        self.update_form_frame.after(10, center_content)
    def perform_update(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="student_admin",
                password="iLove127!",
                database="student_org_database"
            )
            cursor = conn.cursor()
            
            # Get updated values
            updated_fields = {}
            for field, entry in self.update_entries.items():
                new_value = entry.get().strip()
                if new_value and new_value != str(self.current_member[field]):
                    # Convert batch to int if it's the batch field
                    if field == 'batch':
                        try:
                            updated_fields[field] = int(new_value)
                        except ValueError:
                            messagebox.showerror("Error", "Batch must be a valid year (number).")
                            return
                    else:
                        updated_fields[field] = new_value
            
            if not updated_fields:
                messagebox.showinfo("No Changes", "No changes were made.")
                return
            
            # Build update query
            set_clause = ", ".join(f"{field} = %s" for field in updated_fields.keys())
            update_query = f"UPDATE member SET {set_clause} WHERE membership_id = %s"
            params = list(updated_fields.values()) + [self.current_member['membership_id']]
            
            cursor.execute(update_query, tuple(params))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Member updated successfully!")
            
            # Clear the form
            self.search_entry.delete(0, tk.END)
            for widget in self.update_form_frame.winfo_children():
                widget.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    def search_options(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Search Member", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Search input
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        search_label = tk.Label(search_frame, text="Enter Student Number:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        search_label.pack(anchor='w')
        
        search_entry = tk.Entry(search_frame, font=('Segoe UI', 10), 
                               relief='solid', bd=1, bg='#f8f9fa')
        search_entry.pack(fill='x', pady=(5, 0), ipady=5)
        
        # Results area
        results_frame = tk.Frame(self.content_frame, bg='white')
        results_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        results_label = tk.Label(results_frame, text="Search Results:", 
                                font=('Segoe UI', 10, 'bold'), 
                                bg='white', fg='#34495e')
        results_label.pack(anchor='w', pady=(0, 5))
        
        output_box = tk.Text(results_frame, height=12, wrap="word", 
                            font=('Consolas', 9), relief='solid', bd=1,
                            bg='#f8f9fa')
        output_box.pack(fill='both', expand=True)

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

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Search", search, "#3498db")

    def delete_member(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Delete Member", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Warning message
        warning_frame = tk.Frame(self.content_frame, bg='#fff3cd', relief='solid', bd=1)
        warning_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        warning_label = tk.Label(warning_frame, text="⚠️ Warning: This action cannot be undone", 
                                font=('Segoe UI', 10, 'bold'), 
                                bg='#fff3cd', fg='#856404')
        warning_label.pack(pady=10)
        
        # Delete input
        delete_frame = tk.Frame(self.content_frame, bg='white')
        delete_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        delete_label = tk.Label(delete_frame, text="Enter Student Number to Delete:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        delete_label.pack(anchor='w')
        
        delete_entry = tk.Entry(delete_frame, font=('Segoe UI', 10), 
                               relief='solid', bd=1, bg='#f8f9fa')
        delete_entry.pack(fill='x', pady=(5, 0), ipady=5)

        def delete():
            student_number = delete_entry.get()
            if student_number:
                # Confirmation dialog
                if messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete student {student_number}?"):
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
                        delete_entry.delete(0, tk.END)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Missing Input", "Enter a student number.")

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Delete Member", delete, "#e74c3c")

    def show_report_ui(self):
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='white')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="Generate Reports", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='white', fg='#2c3e50')
        title_label.pack()
        
        # Reports grid
        reports_frame = tk.Frame(self.content_frame, bg='white')
        reports_frame.pack(fill='x', padx=30, pady=(0, 20))

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

        for i, (label, action) in enumerate(options):
            btn = tk.Button(reports_frame, text=label, 
                           font=('Segoe UI', 9),
                           bg='#f8f9fa', fg='#2c3e50',
                           relief='solid', bd=1,
                           cursor='hand2',
                           anchor='w',
                           command=action)
            btn.pack(fill='x', pady=2, ipady=8, padx=5)
            
            # Hover effect
            def on_enter(e, button=btn):
                button.configure(bg='#e9ecef')
            
            def on_leave(e, button=btn):
                button.configure(bg='#f8f9fa')
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Output area
        output_frame = tk.Frame(self.content_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        output_label = tk.Label(output_frame, text="Report Output:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_box = tk.Text(output_frame, height=12, wrap="word", 
                                 font=('Consolas', 9), relief='solid', bd=1,
                                 bg='#f8f9fa')
        self.output_box.pack(fill='both', expand=True)

    def run_report(self, func):
        self.output_box.delete("1.0", tk.END)
        try:
            result = capture_output(func)
        except Exception as e:
            result = f"[Error] {e}"
        self.output_box.insert(tk.END, result)

    def report_members_by_org(self):
        self.clear_content()
        
        # Form fields
        fields = ["Organization ID", "Sort By (1=role, 2=status, 3=gender...)"]
        entries = self.create_form_section("View Members by Organization", fields)
        
        org_entry = entries["Organization ID"]
        sort_entry = entries["Sort By (1=role, 2=status, 3=gender...)"]

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

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Run Report", run_custom_query, "#9b59b6")
        
        # Output area
        output_frame = tk.Frame(self.content_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=30, pady=(20, 30))
        
        output_label = tk.Label(output_frame, text="Report Results:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_box = tk.Text(output_frame, height=12, wrap="word", 
                                 font=('Consolas', 9), relief='solid', bd=1,
                                 bg='#f8f9fa')
        self.output_box.pack(fill='both', expand=True)

    def report_unpaid_by_semester(self):
        self.clear_content()
        
        fields = ["Semester (e.g., 2nd)", "Academic Year (e.g., 2024-2025)"]
        entries = self.create_form_section("Unpaid or Late Fees by Semester", fields)
        
        semester_entry = entries["Semester (e.g., 2nd)"]
        year_entry = entries["Academic Year (e.g., 2024-2025)"]

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

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Run Report", run_query, "#9b59b6")
        
        # Output area
        output_frame = tk.Frame(self.content_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=30, pady=(20, 30))
        
        output_label = tk.Label(output_frame, text="Report Results:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_box = tk.Text(output_frame, height=12, wrap="word", 
                                 font=('Consolas', 9), relief='solid', bd=1,
                                 bg='#f8f9fa')
        self.output_box.pack(fill='both', expand=True)

    def report_member_orgs(self):
        self.clear_content()
        
        fields = ["Membership ID"]
        entries = self.create_form_section("View Organizations of a Member", fields)
        
        id_entry = entries["Membership ID"]

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

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Run Report", run_query, "#9b59b6")
        
        # Output area
        output_frame = tk.Frame(self.content_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=30, pady=(20, 30))
        
        output_label = tk.Label(output_frame, text="Report Results:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_box = tk.Text(output_frame, height=12, wrap="word", 
                                 font=('Consolas', 9), relief='solid', bd=1,
                                 bg='#f8f9fa')
        self.output_box.pack(fill='both', expand=True)

    def report_unpaid_by_student(self):
        self.clear_content()
        
        fields = ["Student Number"]
        entries = self.create_form_section("Unpaid/Late Fees by Student Number", fields)
        
        student_entry = entries["Student Number"]

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

        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(padx=30)
        self.create_styled_button(button_frame, "Run Report", run_query, "#9b59b6")
        
        # Output area
        output_frame = tk.Frame(self.content_frame, bg='white')
        output_frame.pack(fill='both', expand=True, padx=30, pady=(20, 30))
        
        output_label = tk.Label(output_frame, text="Report Results:", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='white', fg='#34495e')
        output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_box = tk.Text(output_frame, height=12, wrap="word", 
                                 font=('Consolas', 9), relief='solid', bd=1,
                                 bg='#f8f9fa')
        self.output_box.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()