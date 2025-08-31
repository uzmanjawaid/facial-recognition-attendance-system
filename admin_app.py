"""
Facial Recognition Attendance System - Admin Application
Author: Uzman Jawaid
Description: Administrative panel for managing attendance records and employees
Version: 2.0
Date: August 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from src.database import Database
from src.simple_face_recognition import SimpleFaceRecognizer

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System - Admin Panel")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db = Database()
        self.face_recognizer = SimpleFaceRecognizer()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the admin interface"""
        # Main title
        title_label = tk.Label(self.root, text="👥 ATTENDANCE SYSTEM - ADMIN PANEL", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_attendance_tab()
        self.create_employee_management_tab()
        self.create_reports_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Admin Panel Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_attendance_tab(self):
        """Create the attendance management tab"""
        attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(attendance_frame, text="📅 Attendance Records")
        
        # Filters section
        filter_frame = ttk.LabelFrame(attendance_frame, text="Filters")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filter controls
        controls_frame = ttk.Frame(filter_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(controls_frame, text="From Date:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.from_date_entry = tk.Entry(controls_frame, width=12)
        self.from_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.from_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        tk.Label(controls_frame, text="To Date:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.to_date_entry = tk.Entry(controls_frame, width=12)
        self.to_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.to_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        tk.Label(controls_frame, text="Employee:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.employee_filter_var = tk.StringVar()
        self.employee_filter_combo = ttk.Combobox(controls_frame, textvariable=self.employee_filter_var, 
                                                width=20, state="readonly")
        self.employee_filter_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Filter and export buttons
        filter_btn = ttk.Button(controls_frame, text="🔍 Apply Filter", 
                              command=self.apply_attendance_filter)
        filter_btn.grid(row=0, column=6, padx=10, pady=5)
        
        export_btn = ttk.Button(controls_frame, text="📊 Export CSV", 
                              command=self.export_attendance_csv)
        export_btn.grid(row=0, column=7, padx=5, pady=5)
        
        # Manual time out section
        timeout_frame = ttk.LabelFrame(attendance_frame, text="Manual Time Out")
        timeout_frame.pack(fill=tk.X, padx=10, pady=5)
        
        timeout_controls = ttk.Frame(timeout_frame)
        timeout_controls.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(timeout_controls, text="Currently Checked In:").pack(side=tk.LEFT)
        self.timeout_name_var = tk.StringVar()
        self.timeout_combo = ttk.Combobox(timeout_controls, textvariable=self.timeout_name_var, 
                                        width=25, state="readonly")
        self.timeout_combo.pack(side=tk.LEFT, padx=10)
        
        timeout_btn = ttk.Button(timeout_controls, text="⏰ Mark Time Out", 
                               command=self.manual_time_out)
        timeout_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_checkin_btn = ttk.Button(timeout_controls, text="🔄 Refresh", 
                                       command=self.refresh_checked_in_list)
        refresh_checkin_btn.pack(side=tk.LEFT, padx=5)
        
        # Attendance records table
        records_frame = ttk.LabelFrame(attendance_frame, text="Attendance Records")
        records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for attendance records
        att_columns = ('ID', 'Name', 'Date', 'Time In', 'Time Out', 'Status')
        self.attendance_tree = ttk.Treeview(records_frame, columns=att_columns, show='headings')
        
        for col in att_columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=120)
        
        scrollbar_att = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar_att.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_att.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Statistics
        stats_frame = ttk.LabelFrame(attendance_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Select date range to view statistics", 
                                   font=('Arial', 10))
        self.stats_label.pack(pady=10)
        
        # Initialize
        self.update_employee_filter()
        self.refresh_checked_in_list()
        self.apply_attendance_filter()
    
    def create_employee_management_tab(self):
        """Create employee management tab"""
        emp_frame = ttk.Frame(self.notebook)
        self.notebook.add(emp_frame, text="👥 Employee Management")
        
        # Employee list
        list_frame = ttk.LabelFrame(emp_frame, text="All Employees")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for employees
        emp_columns = ('ID', 'Name', 'Email', 'Phone', 'Department', 'Face Data')
        self.employees_tree = ttk.Treeview(list_frame, columns=emp_columns, show='headings')
        
        for col in emp_columns:
            self.employees_tree.heading(col, text=col)
            if col == 'ID':
                self.employees_tree.column(col, width=50)
            elif col == 'Face Data':
                self.employees_tree.column(col, width=80)
            else:
                self.employees_tree.column(col, width=120)
        
        scrollbar_emp = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.employees_tree.yview)
        self.employees_tree.configure(yscrollcommand=scrollbar_emp.set)
        
        self.employees_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_emp.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Employee management buttons
        emp_buttons_frame = ttk.Frame(emp_frame)
        emp_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_emp_btn = ttk.Button(emp_buttons_frame, text="🔄 Refresh List", 
                                   command=self.refresh_employees_list)
        refresh_emp_btn.pack(side=tk.LEFT, padx=5)
        
        delete_emp_btn = ttk.Button(emp_buttons_frame, text="🗑️ Remove Face Data", 
                                  command=self.remove_face_data)
        delete_emp_btn.pack(side=tk.LEFT, padx=5)
        
        # Statistics
        emp_stats_frame = ttk.LabelFrame(emp_frame, text="Employee Statistics")
        emp_stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.emp_stats_label = tk.Label(emp_stats_frame, text="Loading statistics...", 
                                       font=('Arial', 10))
        self.emp_stats_label.pack(pady=10)
        
        # Load employees
        self.refresh_employees_list()
    
    def create_reports_tab(self):
        """Create reports and analytics tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports & Analytics")
        
        # Quick stats
        quick_stats_frame = ttk.LabelFrame(reports_frame, text="Today's Quick Stats")
        quick_stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.quick_stats_text = tk.Text(quick_stats_frame, height=10, font=('Courier', 10))
        quick_stats_scroll = ttk.Scrollbar(quick_stats_frame, orient=tk.VERTICAL, command=self.quick_stats_text.yview)
        self.quick_stats_text.configure(yscrollcommand=quick_stats_scroll.set)
        
        self.quick_stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        quick_stats_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Report generation
        reports_gen_frame = ttk.LabelFrame(reports_frame, text="Generate Reports")
        reports_gen_frame.pack(fill=tk.X, padx=10, pady=10)
        
        report_buttons = ttk.Frame(reports_gen_frame)
        report_buttons.pack(pady=10)
        
        daily_report_btn = ttk.Button(report_buttons, text="📅 Daily Report", 
                                    command=self.generate_daily_report)
        daily_report_btn.pack(side=tk.LEFT, padx=10)
        
        weekly_report_btn = ttk.Button(report_buttons, text="📊 Weekly Summary", 
                                     command=self.generate_weekly_report)
        weekly_report_btn.pack(side=tk.LEFT, padx=10)
        
        refresh_reports_btn = ttk.Button(report_buttons, text="🔄 Refresh", 
                                       command=self.refresh_reports)
        refresh_reports_btn.pack(side=tk.LEFT, padx=10)
        
        # Initialize reports
        self.refresh_reports()
    
    def manual_time_out(self):
        """Handle manual time out"""
        selected_name = self.timeout_name_var.get()
        
        if not selected_name:
            messagebox.showwarning("Warning", "Please select an employee to check out")
            return
        
        if messagebox.askyesno("Confirm Time Out", f"Mark time out for {selected_name}?"):
            success = self.db.mark_time_out(selected_name)
            
            if success:
                messagebox.showinfo("Success", f"Time out marked for {selected_name}")
                self.refresh_checked_in_list()
                self.apply_attendance_filter()
                self.status_var.set(f"Time out marked for {selected_name}")
            else:
                messagebox.showwarning("Warning", f"{selected_name} is not currently checked in")
    
    def refresh_checked_in_list(self):
        """Refresh the list of currently checked in employees"""
        checked_in = self.db.get_checked_in_employees()
        
        if checked_in:
            employee_names = [f"{name} (In: {time_in})" for name, time_in in checked_in]
            self.timeout_combo['values'] = employee_names
            if employee_names:
                self.timeout_combo.set(employee_names[0])
        else:
            self.timeout_combo['values'] = []
            self.timeout_combo.set("")
    
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
    
    def refresh_employees_list(self):
        """Refresh the employees list"""
        # Clear existing items
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        # Get all employees
        employees = self.db.get_all_employees()
        known_faces = self.face_recognizer.get_known_names()
        
        total_employees = len(employees)
        employees_with_faces = 0
        
        for emp in employees:
            face_status = "✓ Yes" if emp[1] in known_faces else "❌ No"
            if emp[1] in known_faces:
                employees_with_faces += 1
                
            self.employees_tree.insert('', 'end', values=(
                emp[0], emp[1], emp[2], emp[3], emp[4], face_status
            ))
        
        # Update statistics
        stats_text = f"Total Employees: {total_employees} | With Face Data: {employees_with_faces} | Missing Face Data: {total_employees - employees_with_faces}"
        self.emp_stats_label.config(text=stats_text)
    
    def remove_face_data(self):
        """Remove face data for selected employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        item = self.employees_tree.item(selected[0])
        emp_name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Remove face data for {emp_name}?"):
            success = self.face_recognizer.remove_person(emp_name)
            if success:
                messagebox.showinfo("Success", f"Face data removed for {emp_name}")
                self.refresh_employees_list()
            else:
                messagebox.showinfo("Info", f"No face data found for {emp_name}")
    
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
    
    def refresh_reports(self):
        """Refresh the reports tab"""
        self.quick_stats_text.delete(1.0, tk.END)
        
        today = date.today().strftime("%Y-%m-%d")
        today_records = self.db.get_attendance_records(date=today)
        
        self.quick_stats_text.insert(tk.END, f"📊 ADMIN DASHBOARD - {today}\n")
        self.quick_stats_text.insert(tk.END, "=" * 50 + "\n\n")
        
        if today_records:
            checked_in = len([r for r in today_records if not r[5]])
            checked_out = len([r for r in today_records if r[5]])
            
            self.quick_stats_text.insert(tk.END, f"📈 TODAY'S SUMMARY:\n")
            self.quick_stats_text.insert(tk.END, f"   Total attendance records: {len(today_records)}\n")
            self.quick_stats_text.insert(tk.END, f"   Currently at work: {checked_in}\n")
            self.quick_stats_text.insert(tk.END, f"   Completed day: {checked_out}\n\n")
            
            self.quick_stats_text.insert(tk.END, f"👥 EMPLOYEE STATUS:\n")
            for record in today_records:
                name = record[2]
                time_in = record[4]
                time_out = record[5] if record[5] else "Still at work"
                status_icon = "🟢" if record[5] else "🟡"
                
                self.quick_stats_text.insert(tk.END, f"   {status_icon} {name:<20} {time_in} -> {time_out}\n")
        else:
            self.quick_stats_text.insert(tk.END, "No attendance records for today.\n")
    
    def generate_daily_report(self):
        """Generate daily report"""
        messagebox.showinfo("Feature", "Daily report generation coming soon!")
    
    def generate_weekly_report(self):
        """Generate weekly report"""
        messagebox.showinfo("Feature", "Weekly report generation coming soon!")

def main():
    root = tk.Tk()
    
    # Apply modern style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = AdminApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
