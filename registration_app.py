"""
Facial Recognition Attendance System - Registration Application
Author: Uzman Jawaid
Description: Employee registration interface with face capture and setup
Version: 2.0
Date: August 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from src.database import Database
from src.simple_face_recognition import SimpleFaceRecognizer

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System - Employee Registration")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db = Database()
        self.face_recognizer = SimpleFaceRecognizer()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the registration interface"""
        # Main title
        title_label = tk.Label(self.root, text="📝 ATTENDANCE SYSTEM - EMPLOYEE REGISTRATION", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=15)
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel for registration form
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Employee details form
        form_frame = ttk.LabelFrame(left_panel, text="📋 Employee Information")
        form_frame.pack(fill=tk.X, pady=10)
        
        # Create form fields
        form_inner = ttk.Frame(form_frame)
        form_inner.pack(padx=20, pady=15)
        
        # Name (required)
        tk.Label(form_inner, text="Full Name: *", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=8)
        self.name_entry = tk.Entry(form_inner, width=35, font=('Arial', 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=8)
        
        # Email
        tk.Label(form_inner, text="Email Address:").grid(row=1, column=0, sticky='w', padx=5, pady=8)
        self.email_entry = tk.Entry(form_inner, width=35, font=('Arial', 10))
        self.email_entry.grid(row=1, column=1, padx=5, pady=8)
        
        # Phone
        tk.Label(form_inner, text="Phone Number:").grid(row=2, column=0, sticky='w', padx=5, pady=8)
        self.phone_entry = tk.Entry(form_inner, width=35, font=('Arial', 10))
        self.phone_entry.grid(row=2, column=1, padx=5, pady=8)
        
        # Department
        tk.Label(form_inner, text="Department:").grid(row=3, column=0, sticky='w', padx=5, pady=8)
        self.department_entry = tk.Entry(form_inner, width=35, font=('Arial', 10))
        self.department_entry.grid(row=3, column=1, padx=5, pady=8)
        
        # Employee ID (auto-generated info)
        tk.Label(form_inner, text="Employee ID:", fg='gray').grid(row=4, column=0, sticky='w', padx=5, pady=8)
        tk.Label(form_inner, text="(Auto-generated after registration)", fg='gray', font=('Arial', 9)).grid(row=4, column=1, sticky='w', padx=5, pady=8)
        
        # Face registration section
        face_frame = ttk.LabelFrame(left_panel, text="📸 Face Recognition Setup")
        face_frame.pack(fill=tk.X, pady=10)
        
        face_inner = ttk.Frame(face_frame)
        face_inner.pack(padx=20, pady=15)
        
        # Face capture status
        self.face_status_label = tk.Label(face_inner, text="❌ No face data captured", 
                                        fg="red", font=('Arial', 11, 'bold'))
        self.face_status_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(face_inner, 
                               text="Capture face photos for automatic attendance recognition.\nEnsure good lighting and look directly at the camera.",
                               font=('Arial', 9), fg='#666666', justify=tk.CENTER)
        instructions.pack(pady=5)
        
        # Face capture buttons
        button_frame = ttk.Frame(face_inner)
        button_frame.pack(pady=15)
        
        # Method 1: Camera capture (recommended)
        capture_btn = ttk.Button(button_frame, text="📷 Capture from Camera (Recommended)", 
                               command=self.capture_face_from_camera,
                               style='Accent.TButton')
        capture_btn.pack(pady=8)
        
        # Method 2: Upload image
        upload_btn = ttk.Button(button_frame, text="📁 Upload Image File", 
                              command=self.upload_face_image)
        upload_btn.pack(pady=5)
        
        # Registration actions
        action_frame = ttk.LabelFrame(left_panel, text="🚀 Complete Registration")
        action_frame.pack(fill=tk.X, pady=10)
        
        action_inner = ttk.Frame(action_frame)
        action_inner.pack(pady=15)
        
        # Register button
        register_btn = ttk.Button(action_inner, text="✅ Register Employee", 
                                command=self.register_employee,
                                style='Accent.TButton')
        register_btn.pack(pady=10)
        
        # Clear form button
        clear_btn = ttk.Button(action_inner, text="🗑️ Clear Form", 
                             command=self.clear_registration_form)
        clear_btn.pack(pady=5)
        
        # Right panel for employee list and info
        right_panel = ttk.Frame(main_container, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right_panel.pack_propagate(False)
        
        # Recently registered employees
        recent_frame = ttk.LabelFrame(right_panel, text="👥 Recently Registered")
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for recent employees
        emp_columns = ('Name', 'Department', 'Face Data')
        self.recent_tree = ttk.Treeview(recent_frame, columns=emp_columns, show='headings', height=12)
        
        for col in emp_columns:
            self.recent_tree.heading(col, text=col)
            if col == 'Face Data':
                self.recent_tree.column(col, width=80)
            else:
                self.recent_tree.column(col, width=100)
        
        scrollbar_recent = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar_recent.set)
        
        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_recent.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Statistics and actions
        stats_frame = ttk.LabelFrame(right_panel, text="📊 Registration Stats")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Loading statistics...", 
                                   font=('Arial', 10), wraplength=320, justify=tk.CENTER)
        self.stats_label.pack(pady=15)
        
        # Action buttons for list management
        list_actions_frame = ttk.Frame(right_panel)
        list_actions_frame.pack(fill=tk.X, pady=5)
        
        refresh_btn = ttk.Button(list_actions_frame, text="🔄 Refresh List", 
                               command=self.refresh_employees_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        remove_face_btn = ttk.Button(list_actions_frame, text="🗑️ Remove Face", 
                                   command=self.remove_selected_face)
        remove_face_btn.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready for employee registration")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load initial data
        self.refresh_employees_list()
        
        # Focus on name field
        self.name_entry.focus()
    
    def capture_face_from_camera(self):
        """Capture face images from camera for registration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter employee name first")
            self.name_entry.focus()
            return
        
        # Confirmation dialog
        if not messagebox.askyesno("Camera Capture", 
                                  f"Start camera to capture face photos for {name}?\n\n" +
                                  "Instructions:\n" +
                                  "• Look directly at the camera\n" +
                                  "• Ensure good lighting\n" +
                                  "• Press SPACE to take each photo\n" +
                                  "• 5 photos will be captured"):
            return
        
        try:
            success = self.face_recognizer.capture_face_for_training(name)
            if success:
                messagebox.showinfo("Success", 
                                  f"Face photos captured successfully for {name}!\n\n" +
                                  "✅ Face recognition is now ready\n" +
                                  "Click 'Register Employee' to save all details.")
                
                # Update face status indicator
                self.face_status_label.config(text="✅ Face data captured", fg="green")
                self.status_var.set(f"Face data captured for {name} - Ready to register")
                
            else:
                messagebox.showerror("Error", "Failed to capture face images.\n\nPlease try again or use 'Upload Image' option.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Camera error: {str(e)}")
    
    def upload_face_image(self):
        """Upload face image for registration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter employee name first")
            self.name_entry.focus()
            return
        
        file_path = filedialog.askopenfilename(
            title="Select face image for " + name,
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                success = self.face_recognizer.add_new_face(file_path, name)
                if success:
                    messagebox.showinfo("Success", 
                                      f"Face image uploaded successfully for {name}!\n\n" +
                                      "✅ Face recognition is now ready\n" +
                                      "Click 'Register Employee' to save all details.")
                    
                    # Update face status indicator
                    self.face_status_label.config(text="✅ Face image uploaded", fg="green")
                    self.status_var.set(f"Face data uploaded for {name} - Ready to register")
                    
                else:
                    messagebox.showerror("Error", 
                                       "Failed to process face image.\n\n" +
                                       "Please ensure:\n" +
                                       "• Image contains exactly one clear face\n" +
                                       "• Good lighting and image quality\n" +
                                       "• Face is not obstructed")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Image processing error: {str(e)}")
    
    def register_employee(self):
        """Register employee in database"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        department = self.department_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Employee name is required")
            self.name_entry.focus()
            return
        
        # Check if face data exists
        known_faces = self.face_recognizer.get_known_names()
        has_face_data = name in known_faces
        
        # Confirm registration
        face_status_text = "✅ Face recognition: Ready" if has_face_data else "❌ Face recognition: Not set up"
        
        if not messagebox.askyesno("Confirm Registration", 
                                  f"Register employee with the following details?\n\n" +
                                  f"Name: {name}\n" +
                                  f"Email: {email or 'Not provided'}\n" +
                                  f"Phone: {phone or 'Not provided'}\n" +
                                  f"Department: {department or 'Not provided'}\n\n" +
                                  f"{face_status_text}"):
            return
        
        try:
            employee_id = self.db.add_employee(name, email, phone, department)
            if employee_id:
                if has_face_data:
                    messagebox.showinfo("Registration Successful!", 
                                      f"Employee registered successfully!\n\n" +
                                      f"👤 Name: {name}\n" +
                                      f"🆔 Employee ID: {employee_id}\n" +
                                      f"✅ Face recognition: Ready\n\n" +
                                      f"Employee can now use attendance system.")
                else:
                    messagebox.showinfo("Registration Successful!", 
                                      f"Employee registered successfully!\n\n" +
                                      f"👤 Name: {name}\n" +
                                      f"🆔 Employee ID: {employee_id}\n" +
                                      f"⚠️  Face recognition: Not set up\n\n" +
                                      f"Note: Capture face photos for automatic attendance.")
                
                # Clear form and refresh list
                self.clear_registration_form()
                self.refresh_employees_list()
                self.status_var.set(f"Employee {name} registered successfully (ID: {employee_id})")
                
                # Focus back to name field for next registration
                self.name_entry.focus()
                
            else:
                messagebox.showerror("Registration Failed", 
                                   f"Employee name '{name}' already exists in the system.\n\n" +
                                   "Please use a different name or check existing records.")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to register employee: {str(e)}")
    
    def clear_registration_form(self):
        """Clear the registration form"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        
        # Reset face status indicator
        self.face_status_label.config(text="❌ No face data captured", fg="red")
        self.status_var.set("Form cleared - Ready for new employee registration")
    
    def refresh_employees_list(self):
        """Refresh the employees list"""
        # Clear existing items
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        try:
            # Get all employees (limit to recent 20 for display)
            employees = self.db.get_all_employees()
            known_faces = self.face_recognizer.get_known_names()
            
            # Sort by ID descending to show most recent first
            employees = sorted(employees, key=lambda x: x[0], reverse=True)
            recent_employees = employees[:20]  # Show only recent 20
            
            total_employees = len(employees)
            employees_with_faces = 0
            
            for emp in recent_employees:
                face_status = "✅ Yes" if emp[1] in known_faces else "❌ No"
                if emp[1] in known_faces:
                    employees_with_faces += 1
                    
                # Display name, department, and face status
                self.recent_tree.insert('', 'end', values=(
                    emp[1],  # name
                    emp[4] or 'Not specified',  # department
                    face_status  # face data status
                ))
            
            # Count total employees with face data
            total_with_faces = len([emp for emp in employees if emp[1] in known_faces])
            
            # Update statistics
            stats_text = (f"📊 Registration Statistics:\n\n" +
                         f"Total Employees: {total_employees}\n" +
                         f"With Face Data: {total_with_faces}\n" +
                         f"Missing Face Data: {total_employees - total_with_faces}\n\n" +
                         f"Showing {len(recent_employees)} most recent")
            
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh employee list: {str(e)}")
    
    def remove_selected_face(self):
        """Remove face data for selected employee"""
        selected = self.recent_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee from the list first.")
            return
        
        item = self.recent_tree.item(selected[0])
        emp_name = item['values'][0]
        
        if messagebox.askyesno("Confirm Face Data Removal", 
                              f"Remove face recognition data for {emp_name}?\n\n" +
                              "This will:\n" +
                              "• Delete all stored face photos\n" +
                              "• Remove face recognition templates\n" +
                              "• Require re-capturing photos for attendance\n\n" +
                              "Employee database record will remain unchanged."):
            
            try:
                success = self.face_recognizer.remove_person(emp_name)
                if success:
                    messagebox.showinfo("Success", f"Face recognition data removed for {emp_name}")
                    self.refresh_employees_list()
                    self.status_var.set(f"Face data removed for {emp_name}")
                else:
                    messagebox.showinfo("No Data Found", f"No face recognition data found for {emp_name}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove face data: {str(e)}")

def main():
    root = tk.Tk()
    
    # Apply modern style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom button style
    style.configure('Accent.TButton', 
                   font=('Arial', 10, 'bold'))
    
    app = RegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
