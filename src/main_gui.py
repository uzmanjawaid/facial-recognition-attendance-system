import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime, date
from src.database import Database
from src.simple_face_recognition import SimpleFaceRecognizer

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Recognition Attendance System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db = Database()
        self.face_recognizer = SimpleFaceRecognizer()
        
        # Camera variables
        self.cap = None
        self.camera_running = False
        self.video_thread = None
        
        # UI variables
        self.current_frame = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_attendance_tab()
        self.create_registration_tab()
        self.create_admin_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_attendance_tab(self):
        """Create the attendance marking tab"""
        attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(attendance_frame, text="Mark Attendance")
        
        # Left panel for camera
        left_panel = ttk.Frame(attendance_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Camera frame
        camera_frame = ttk.LabelFrame(left_panel, text="Camera View")
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.camera_label = tk.Label(camera_frame, text="Camera not started", 
                                   bg='gray', width=80, height=30)
        self.camera_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Camera controls
        controls_frame = ttk.Frame(left_panel)
        controls_frame.pack(fill=tk.X, pady=5)
        
        self.start_camera_btn = ttk.Button(controls_frame, text="Start Camera", 
                                         command=self.start_camera)
        self.start_camera_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_camera_btn = ttk.Button(controls_frame, text="Stop Camera", 
                                        command=self.stop_camera, state=tk.DISABLED)
        self.stop_camera_btn.pack(side=tk.LEFT, padx=5)
        
        # Manual time out controls
        timeout_frame = ttk.LabelFrame(left_panel, text="Manual Time Out")
        timeout_frame.pack(fill=tk.X, pady=5)
        
        timeout_controls = ttk.Frame(timeout_frame)
        timeout_controls.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(timeout_controls, text="Employee:").pack(side=tk.LEFT)
        self.timeout_name_var = tk.StringVar()
        self.timeout_combo = ttk.Combobox(timeout_controls, textvariable=self.timeout_name_var, 
                                        width=20, state="readonly")
        self.timeout_combo.pack(side=tk.LEFT, padx=5)
        
        timeout_btn = ttk.Button(timeout_controls, text="Mark Time Out", 
                               command=self.manual_time_out)
        timeout_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_checkin_btn = ttk.Button(timeout_controls, text="Refresh", 
                                       command=self.refresh_checked_in_list)
        refresh_checkin_btn.pack(side=tk.LEFT, padx=5)
        
        # Currently checked in employees
        checkin_frame = ttk.LabelFrame(left_panel, text="Currently Checked In")
        checkin_frame.pack(fill=tk.X, pady=5)
        
        self.checkin_listbox = tk.Listbox(checkin_frame, height=4)
        checkin_scrollbar = ttk.Scrollbar(checkin_frame, orient=tk.VERTICAL, command=self.checkin_listbox.yview)
        self.checkin_listbox.configure(yscrollcommand=checkin_scrollbar.set)
        
        self.checkin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        checkin_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Initialize the lists
        self.refresh_checked_in_list()
        
        # Right panel for information
        right_panel = ttk.Frame(attendance_frame, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        right_panel.pack_propagate(False)
        
        # Today's attendance
        today_frame = ttk.LabelFrame(right_panel, text="Today's Attendance")
        today_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for today's attendance
        columns = ('Name', 'Time In', 'Time Out', 'Status')
        self.today_tree = ttk.Treeview(today_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.today_tree.heading(col, text=col)
            self.today_tree.column(col, width=70)
        
        scrollbar_today = ttk.Scrollbar(today_frame, orient=tk.VERTICAL, command=self.today_tree.yview)
        self.today_tree.configure(yscrollcommand=scrollbar_today.set)
        
        self.today_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_today.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        refresh_btn = ttk.Button(right_panel, text="Refresh Today's Attendance", 
                               command=self.refresh_today_attendance)
        refresh_btn.pack(pady=5)
        
        # Load today's attendance
        self.refresh_today_attendance()
    
    def create_registration_tab(self):
        """Create the employee registration tab"""
        registration_frame = ttk.Frame(self.notebook)
        self.notebook.add(registration_frame, text="Register Employee")
        
        # Left panel for form
        left_panel = ttk.Frame(registration_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Employee details form
        form_frame = ttk.LabelFrame(left_panel, text="Employee Details")
        form_frame.pack(fill=tk.X, pady=10)
        
        # Name
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Phone
        tk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Department
        tk.Label(form_frame, text="Department:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.department_entry = tk.Entry(form_frame, width=30)
        self.department_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Face registration methods
        face_frame = ttk.LabelFrame(left_panel, text="Face Registration")
        face_frame.pack(fill=tk.X, pady=10)
        
        # Face capture status
        self.face_status_label = tk.Label(face_frame, text="❌ No face data captured", 
                                        fg="red", font=('Arial', 9))
        self.face_status_label.pack(pady=5)
        
        # Method 1: Camera capture
        capture_btn = ttk.Button(face_frame, text="Capture from Camera", 
                               command=self.capture_face_from_camera)
        capture_btn.pack(pady=5)
        
        # Method 2: Upload image
        upload_btn = ttk.Button(face_frame, text="Upload Image", 
                              command=self.upload_face_image)
        upload_btn.pack(pady=5)
        
        # Register button
        register_btn = ttk.Button(left_panel, text="Register Employee", 
                                command=self.register_employee)
        register_btn.pack(pady=10)
        
        # Right panel for employee list
        right_panel = ttk.Frame(registration_frame, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        # Registered employees list
        employees_frame = ttk.LabelFrame(right_panel, text="Registered Employees")
        employees_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for employees
        emp_columns = ('ID', 'Name', 'Email', 'Department')
        self.employees_tree = ttk.Treeview(employees_frame, columns=emp_columns, show='headings')
        
        for col in emp_columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=90)
        
        scrollbar_emp = ttk.Scrollbar(employees_frame, orient=tk.VERTICAL, command=self.employees_tree.yview)
        self.employees_tree.configure(yscrollcommand=scrollbar_emp.set)
        
        self.employees_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_emp.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons for employee management
        emp_buttons_frame = ttk.Frame(right_panel)
        emp_buttons_frame.pack(fill=tk.X, pady=5)
        
        refresh_emp_btn = ttk.Button(emp_buttons_frame, text="Refresh", 
                                   command=self.refresh_employees_list)
        refresh_emp_btn.pack(side=tk.LEFT, padx=2)
        
        delete_emp_btn = ttk.Button(emp_buttons_frame, text="Delete Selected", 
                                  command=self.delete_employee)
        delete_emp_btn.pack(side=tk.LEFT, padx=2)
        
        # Load employees list
        self.refresh_employees_list()
    
    def create_admin_tab(self):
        """Create the admin panel tab"""
        admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(admin_frame, text="Admin Panel")
        
        # Top frame for date filters
        filter_frame = ttk.LabelFrame(admin_frame, text="Filters")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(filter_frame, text="From Date:").grid(row=0, column=0, padx=5, pady=5)
        self.from_date_entry = tk.Entry(filter_frame, width=12)
        self.from_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.from_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        tk.Label(filter_frame, text="To Date:").grid(row=0, column=2, padx=5, pady=5)
        self.to_date_entry = tk.Entry(filter_frame, width=12)
        self.to_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.to_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        tk.Label(filter_frame, text="Employee:").grid(row=0, column=4, padx=5, pady=5)
        self.employee_filter_var = tk.StringVar()
        self.employee_filter_combo = ttk.Combobox(filter_frame, textvariable=self.employee_filter_var, 
                                                width=15, state="readonly")
        self.employee_filter_combo.grid(row=0, column=5, padx=5, pady=5)
        
        filter_btn = ttk.Button(filter_frame, text="Apply Filter", 
                              command=self.apply_attendance_filter)
        filter_btn.grid(row=0, column=6, padx=10, pady=5)
        
        export_btn = ttk.Button(filter_frame, text="Export to CSV", 
                              command=self.export_attendance_csv)
        export_btn.grid(row=0, column=7, padx=5, pady=5)
        
        # Attendance records
        records_frame = ttk.LabelFrame(admin_frame, text="Attendance Records")
        records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for attendance records
        att_columns = ('ID', 'Name', 'Date', 'Time In', 'Time Out', 'Status')
        self.attendance_tree = ttk.Treeview(records_frame, columns=att_columns, show='headings')
        
        for col in att_columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=100)
        
        scrollbar_att = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar_att.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_att.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(admin_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Select date range to view statistics", 
                                   font=('Arial', 10))
        self.stats_label.pack(pady=10)
        
        # Initialize filters
        self.update_employee_filter()
        self.apply_attendance_filter()
    
    def start_camera(self):
        """Start the camera for face recognition"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera")
            return
        
        self.camera_running = True
        self.start_camera_btn.config(state=tk.DISABLED)
        self.stop_camera_btn.config(state=tk.NORMAL)
        
        # Start video thread
        self.video_thread = threading.Thread(target=self.video_loop)
        self.video_thread.daemon = True
        self.video_thread.start()
        
        self.status_var.set("Camera started - Looking for faces...")
    
    def stop_camera(self):
        """Stop the camera"""
        self.camera_running = False
        if self.cap:
            self.cap.release()
        
        self.start_camera_btn.config(state=tk.NORMAL)
        self.stop_camera_btn.config(state=tk.DISABLED)
        self.camera_label.config(image='', text="Camera stopped")
        self.status_var.set("Camera stopped")
    
    def video_loop(self):
        """Main video processing loop"""
        while self.camera_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Recognize faces
            recognized_faces = self.face_recognizer.recognize_faces_in_frame(frame)
            
            # Draw rectangles and names
            for name, (top, right, bottom, left), confidence in recognized_faces:
                # Get employee status
                status, time_in, time_out = None, None, None
                if name != "Unknown":
                    status, time_in, time_out = self.get_employee_current_status(name)
                
                # Draw rectangle around face
                if name == "Unknown":
                    color = (0, 0, 255)  # Red for unknown
                elif status == "checked_in":
                    color = (0, 255, 255)  # Yellow for checked in
                elif status == "checked_out":
                    color = (0, 255, 0)  # Green for checked out
                else:
                    color = (255, 0, 0)  # Blue for not present today
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw label with status
                if name != "Unknown":
                    if status == "checked_in":
                        label = f"{name} - IN ({time_in})"
                    elif status == "checked_out":
                        label = f"{name} - OUT ({time_out})"
                    else:
                        label = f"{name} - Not marked today"
                else:
                    label = name
                
                # Calculate label background size
                (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
                cv2.rectangle(frame, (left, bottom - label_height - 10), (left + label_width + 10, bottom), color, cv2.FILLED)
                cv2.putText(frame, label, (left + 5, bottom - 5), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                
                # Mark attendance for known faces with high confidence
                if name != "Unknown" and confidence > 0.6:
                    self.mark_attendance_smart(name, status)
            
            # Convert frame to PIL format for tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_pil = frame_pil.resize((800, 600), Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update the label
            self.camera_label.config(image=frame_tk, text='')
            self.camera_label.image = frame_tk
        
        # Cleanup when loop ends
        if self.cap:
            self.cap.release()
    
    def mark_attendance_async(self, name):
        """Mark attendance asynchronously (legacy method)"""
        try:
            success = self.db.mark_attendance(name)
            if success:
                self.root.after(0, lambda: self.status_var.set(f"Attendance marked for {name}"))
                self.root.after(0, self.refresh_today_attendance)
                self.root.after(0, self.refresh_checked_in_list)
        except Exception as e:
            print(f"Error marking attendance: {e}")
    
    def mark_attendance_smart(self, name, current_status):
        """Smart attendance marking that only marks when appropriate"""
        # Use a simple throttling mechanism to avoid multiple rapid marks
        current_time = datetime.now()
        
        # Only mark attendance every 10 seconds for the same person
        if hasattr(self, '_last_recognition'):
            if name in self._last_recognition:
                time_diff = (current_time - self._last_recognition[name]).total_seconds()
                if time_diff < 10:  # 10 second cooldown
                    return
        else:
            self._last_recognition = {}
        
        self._last_recognition[name] = current_time
        
        try:
            if current_status == "not_present":
                # First time today - mark time in
                success = self.db.mark_attendance(name)
                if success:
                    self.root.after(0, lambda: self.status_var.set(f"Time IN marked for {name}"))
                    self.root.after(0, self.refresh_today_attendance)
                    self.root.after(0, self.refresh_checked_in_list)
            elif current_status == "checked_in":
                # Already checked in - could auto mark time out after certain period
                # For now, just update status to show they're still present
                self.root.after(0, lambda: self.status_var.set(f"{name} is already checked in"))
            elif current_status == "checked_out":
                # Already checked out - could mark as return
                self.root.after(0, lambda: self.status_var.set(f"{name} already checked out today"))
                
        except Exception as e:
            print(f"Error in smart attendance marking: {e}")
    
    def manual_time_out(self):
        """Handle manual time out for selected employee"""
        selected_name = self.timeout_name_var.get()
        
        if not selected_name:
            messagebox.showwarning("Warning", "Please select an employee to check out")
            return
        
        # Confirm the action
        if messagebox.askyesno("Confirm Time Out", f"Mark time out for {selected_name}?"):
            success = self.db.mark_time_out(selected_name)
            
            if success:
                messagebox.showinfo("Success", f"Time out marked for {selected_name}")
                self.refresh_checked_in_list()
                self.refresh_today_attendance()
                self.status_var.set(f"Time out marked for {selected_name}")
            else:
                messagebox.showwarning("Warning", f"{selected_name} is not currently checked in")
    
    def refresh_checked_in_list(self):
        """Refresh the list of currently checked in employees"""
        # Clear existing items
        self.checkin_listbox.delete(0, tk.END)
        self.timeout_combo['values'] = []
        
        # Get currently checked in employees
        checked_in = self.db.get_checked_in_employees()
        
        if checked_in:
            employee_names = []
            for name, time_in in checked_in:
                display_text = f"{name} (In: {time_in})"
                self.checkin_listbox.insert(tk.END, display_text)
                employee_names.append(name)
            
            # Update timeout combo
            self.timeout_combo['values'] = employee_names
            if employee_names:
                self.timeout_combo.set(employee_names[0])
        else:
            self.checkin_listbox.insert(tk.END, "No employees currently checked in")
    
    def refresh_today_attendance(self):
        """Refresh today's attendance list"""
        # Clear existing items
        for item in self.today_tree.get_children():
            self.today_tree.delete(item)
        
        # Get today's records
        today = date.today().strftime("%Y-%m-%d")
        records = self.db.get_attendance_records(date=today)
        
        for record in records:
            # Format: (id, employee_id, name, date, time_in, time_out, status, created_at)
            time_out = record[5] if record[5] else "Not marked"
            self.today_tree.insert('', 'end', values=(record[2], record[4], time_out, record[6]))
    
    def capture_face_from_camera(self):
        """Capture face images from camera for registration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter employee name first")
            return
        
        success = self.face_recognizer.capture_face_for_training(name)
        if success:
            messagebox.showinfo("Success", f"Face captured for {name}!\n\nNow click 'Register Employee' to save details to database.")
            # Update face status indicator
            self.face_status_label.config(text="✓ Face data captured", fg="green")
            # Don't clear form - user may want to register employee details too
        else:
            messagebox.showerror("Error", "Failed to capture face images")
    
    def upload_face_image(self):
        """Upload face image for registration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter employee name first")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select face image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            success = self.face_recognizer.add_new_face(file_path, name)
            if success:
                messagebox.showinfo("Success", f"Face image uploaded for {name}!\n\nNow click 'Register Employee' to save details to database.")
                # Update face status indicator
                self.face_status_label.config(text="✓ Face data uploaded", fg="green")
                # Don't clear form - user may want to register employee details too
            else:
                messagebox.showerror("Error", "Failed to process face image")
    
    def register_employee(self):
        """Register employee in database"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        department = self.department_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        
    def register_employee(self):
        """Register employee in database"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        department = self.department_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        
        # Check if face data exists
        known_faces = self.face_recognizer.get_known_names()
        has_face_data = name in known_faces
        
        employee_id = self.db.add_employee(name, email, phone, department)
        if employee_id:
            if has_face_data:
                messagebox.showinfo("Success", f"Employee {name} registered successfully!\n\nFace recognition data: ✓ Available\nReady for attendance tracking.")
            else:
                messagebox.showinfo("Success", f"Employee {name} registered successfully!\n\nFace recognition data: ❌ Not available\nCapture face images for attendance tracking.")
            self.clear_registration_form()
            self.refresh_employees_list()
        else:
            messagebox.showerror("Error", "Employee name already exists")
    
    def clear_registration_form(self):
        """Clear the registration form"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        # Reset face status indicator
        self.face_status_label.config(text="❌ No face data captured", fg="red")
    
    def refresh_employees_list(self):
        """Refresh the employees list"""
        # Clear existing items
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        # Get all employees
        employees = self.db.get_all_employees()
        for emp in employees:
            self.employees_tree.insert('', 'end', values=(emp[0], emp[1], emp[2], emp[4]))
    
    def delete_employee(self):
        """Delete selected employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        item = self.employees_tree.item(selected[0])
        emp_name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Delete employee {emp_name}?"):
            # Remove from face recognition database
            self.face_recognizer.remove_person(emp_name)
            # Note: We're not deleting from employees table to maintain referential integrity
            messagebox.showinfo("Info", f"Face data removed for {emp_name}")
            self.refresh_employees_list()
    
    def update_employee_filter(self):
        """Update employee filter dropdown"""
        employees = self.db.get_all_employees()
        employee_names = ["All"] + [emp[1] for emp in employees]
        self.employee_filter_combo['values'] = employee_names
        self.employee_filter_combo.set("All")
    
    def apply_attendance_filter(self):
        """Apply filters to attendance records"""
        # Clear existing items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        employee_filter = self.employee_filter_var.get()
        
        # Get filtered records
        if employee_filter == "All" or not employee_filter:
            records = self.db.get_attendance_records()
        else:
            records = self.db.get_attendance_records(name=employee_filter)
        
        # Filter by date range
        filtered_records = []
        for record in records:
            record_date = record[3]  # date column
            if from_date <= record_date <= to_date:
                filtered_records.append(record)
        
        # Populate tree
        for record in filtered_records:
            time_out = record[5] if record[5] else "Not marked"
            self.attendance_tree.insert('', 'end', values=(
                record[0], record[2], record[3], record[4], time_out, record[6]
            ))
        
        # Update statistics
        self.update_statistics(filtered_records)
    
    def update_statistics(self, records):
        """Update statistics display"""
        total_records = len(records)
        unique_employees = len(set(record[2] for record in records))
        present_today = len([r for r in records if r[3] == date.today().strftime("%Y-%m-%d")])
        
        stats_text = f"Total Records: {total_records} | Unique Employees: {unique_employees} | Present Today: {present_today}"
        self.stats_label.config(text=stats_text)
    
    def export_attendance_csv(self):
        """Export attendance records to CSV"""
        import csv
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save attendance report"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Name', 'Date', 'Time In', 'Time Out', 'Status'])
                    
                    for child in self.attendance_tree.get_children():
                        values = self.attendance_tree.item(child)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Success", f"Attendance report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def refresh_checked_in_list(self):
        """Refresh the list of currently checked in employees"""
        # Clear existing items
        self.checkin_listbox.delete(0, tk.END)
        self.timeout_combo['values'] = []
        
        # Get currently checked in employees
        checked_in = self.db.get_checked_in_employees()
        
        if checked_in:
            employee_names = []
            for name, time_in in checked_in:
                display_text = f"{name} (In: {time_in})"
                self.checkin_listbox.insert(tk.END, display_text)
                employee_names.append(name)
            
            # Update timeout combo
            self.timeout_combo['values'] = employee_names
            if employee_names:
                self.timeout_combo.set(employee_names[0])
        else:
            self.checkin_listbox.insert(tk.END, "No employees currently checked in")
    
    def manual_time_out(self):
        """Handle manual time out for selected employee"""
        selected_name = self.timeout_name_var.get()
        
        if not selected_name:
            messagebox.showwarning("Warning", "Please select an employee to check out")
            return
        
        # Confirm the action
        if messagebox.askyesno("Confirm Time Out", f"Mark time out for {selected_name}?"):
            success = self.db.mark_time_out(selected_name)
            
            if success:
                messagebox.showinfo("Success", f"Time out marked for {selected_name}")
                self.refresh_checked_in_list()
                self.refresh_today_attendance()
                self.status_var.set(f"Time out marked for {selected_name}")
            else:
                messagebox.showwarning("Warning", f"{selected_name} is not currently checked in")
    
    def get_employee_current_status(self, name):
        """Get current status of an employee"""
        status, time_in, time_out = self.db.get_employee_status(name)
        return status, time_in, time_out
    
    def on_closing(self):
        """Handle application closing"""
        if self.camera_running:
            self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
