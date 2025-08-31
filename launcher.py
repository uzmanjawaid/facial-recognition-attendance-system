"""
Facial Recognition Attendance System - Application Launcher
Author: Uzman Jawaid
Description: Central launcher for accessing all attendance system modules
Version: 2.0
Date: August 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class AttendanceLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System - Application Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the launcher interface"""
        # Main container with background
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🏢 ATTENDANCE SYSTEM", 
                              font=('Arial', 24, 'bold'),
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, 
                                 text="Choose Your Application Module", 
                                 font=('Arial', 12),
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack(pady=(5, 0))
        
        # Applications frame
        apps_frame = tk.Frame(main_frame, bg='#2c3e50')
        apps_frame.pack(fill='both', expand=True)
        
        # Define applications with their details
        apps = [
            {
                'title': '👤 User Application',
                'subtitle': 'Mark Attendance',
                'description': 'Simple interface for employees to\nmark their attendance using face\nrecognition or manual check-in.',
                'file': 'user_app.py',
                'color': '#27ae60',
                'hover_color': '#2ecc71',
                'features': ['• Quick attendance marking', '• Face recognition', '• Time in/out tracking', '• Personal attendance status']
            },
            {
                'title': '👨‍💼 Admin Application',
                'subtitle': 'Manage System',
                'description': 'Administrative panel for viewing\nattendance records, generating\nreports, and managing employees.',
                'file': 'admin_app.py',
                'color': '#3498db',
                'hover_color': '#2980b9',
                'features': ['• View attendance records', '• Generate reports', '• Employee management', '• System statistics']
            },
            {
                'title': '📝 Registration App',
                'subtitle': 'Setup Employees',
                'description': 'Employee registration interface\nfor adding new employees and\nsetting up face recognition.',
                'file': 'registration_app.py',
                'color': '#e74c3c',
                'hover_color': '#c0392b',
                'features': ['• Register new employees', '• Capture face photos', '• Setup face recognition', '• Manage employee data']
            }
        ]
        
        # Create application cards in a grid
        for i, app in enumerate(apps):
            row = i // 2
            col = i % 2
            
            # Create card frame
            card_frame = tk.Frame(apps_frame, bg=app['color'], relief='raised', bd=2)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew', ipadx=15, ipady=15)
            
            # Configure grid weights for responsive design
            apps_frame.grid_rowconfigure(row, weight=1)
            apps_frame.grid_columnconfigure(col, weight=1)
            
            # App title
            title_label = tk.Label(card_frame, 
                                  text=app['title'], 
                                  font=('Arial', 16, 'bold'),
                                  fg='white', bg=app['color'])
            title_label.pack(anchor='w', pady=(0, 5))
            
            # App subtitle
            subtitle_label = tk.Label(card_frame, 
                                     text=app['subtitle'], 
                                     font=('Arial', 10, 'italic'),
                                     fg='#ecf0f1', bg=app['color'])
            subtitle_label.pack(anchor='w', pady=(0, 10))
            
            # App description
            desc_label = tk.Label(card_frame, 
                                 text=app['description'],
                                 font=('Arial', 9),
                                 fg='white', bg=app['color'],
                                 justify='left')
            desc_label.pack(anchor='w', pady=(0, 10))
            
            # Features list
            features_label = tk.Label(card_frame, 
                                     text='\n'.join(app['features']),
                                     font=('Arial', 8),
                                     fg='#ecf0f1', bg=app['color'],
                                     justify='left')
            features_label.pack(anchor='w', pady=(0, 15))
            
            # Launch button
            launch_btn = tk.Button(card_frame, 
                                  text=f"🚀 Launch {app['subtitle']}", 
                                  font=('Arial', 10, 'bold'),
                                  fg=app['color'], bg='white',
                                  relief='flat', bd=0,
                                  padx=20, pady=8,
                                  cursor='hand2',
                                  command=lambda f=app['file']: self.launch_app(f))
            launch_btn.pack(anchor='center')
            
            # Add hover effects
            def on_enter(event, btn=launch_btn, color=app['hover_color']):
                btn.configure(fg=color)
            
            def on_leave(event, btn=launch_btn, color=app['color']):
                btn.configure(fg=color)
            
            launch_btn.bind("<Enter>", on_enter)
            launch_btn.bind("<Leave>", on_leave)
        
        # Footer section
        footer_frame = tk.Frame(main_frame, bg='#2c3e50')
        footer_frame.pack(fill='x', pady=(30, 0))
        
        # Instructions
        instructions_label = tk.Label(footer_frame, 
                                     text="💡 Choose the appropriate application based on your role and requirements",
                                     font=('Arial', 9, 'italic'),
                                     fg='#95a5a6', bg='#2c3e50')
        instructions_label.pack()
        
        # System info
        info_frame = tk.Frame(footer_frame, bg='#2c3e50')
        info_frame.pack(fill='x', pady=(15, 0))
        
        # Exit and info buttons
        button_frame = tk.Frame(info_frame, bg='#2c3e50')
        button_frame.pack()
        
        info_btn = tk.Button(button_frame, 
                            text="ℹ️ System Info", 
                            font=('Arial', 9),
                            fg='#7f8c8d', bg='#34495e',
                            relief='flat', bd=0,
                            padx=15, pady=5,
                            cursor='hand2',
                            command=self.show_system_info)
        info_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(button_frame, 
                           text="❌ Exit Launcher", 
                           font=('Arial', 9),
                           fg='#e74c3c', bg='#34495e',
                           relief='flat', bd=0,
                           padx=15, pady=5,
                           cursor='hand2',
                           command=self.exit_launcher)
        exit_btn.pack(side=tk.LEFT, padx=5)
    
    def launch_app(self, app_file):
        """Launch the selected application"""
        try:
            # Check if file exists
            if not os.path.exists(app_file):
                messagebox.showerror("File Not Found", 
                                   f"Application file '{app_file}' not found.\n\n" +
                                   "Please ensure all application files are in the current directory.")
                return
            
            # Show loading message
            app_names = {
                'user_app.py': 'User Application',
                'admin_app.py': 'Admin Application', 
                'registration_app.py': 'Registration Application'
            }
            
            app_name = app_names.get(app_file, app_file)
            
            # Minimize launcher window
            self.root.iconify()
            
            # Launch the application
            subprocess.run([sys.executable, app_file], check=True)
            
            # Restore launcher window when app closes
            self.root.deiconify()
            self.root.lift()
            
        except subprocess.CalledProcessError as e:
            self.root.deiconify()
            messagebox.showerror("Launch Error", 
                               f"Failed to launch {app_name}.\n\n" +
                               f"Error: {str(e)}\n\n" +
                               "Please check that Python and required modules are properly installed.")
        except FileNotFoundError:
            self.root.deiconify()
            messagebox.showerror("Python Not Found", 
                               "Python interpreter not found.\n\n" +
                               "Please ensure Python is properly installed and added to system PATH.")
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Unexpected Error", 
                               f"An unexpected error occurred:\n\n{str(e)}")
    
    def show_system_info(self):
        """Show system information dialog"""
        try:
            # Get Python version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            
            # Check for key modules
            modules_status = []
            required_modules = ['tkinter', 'cv2', 'PIL', 'sqlite3', 'threading', 'datetime']
            
            for module in required_modules:
                try:
                    if module == 'cv2':
                        import cv2
                        version = cv2.__version__
                        modules_status.append(f"✅ OpenCV: {version}")
                    elif module == 'PIL':
                        import PIL
                        version = PIL.__version__
                        modules_status.append(f"✅ Pillow: {version}")
                    else:
                        __import__(module)
                        modules_status.append(f"✅ {module}: Available")
                except ImportError:
                    modules_status.append(f"❌ {module}: Not installed")
            
            # Check application files
            app_files = ['user_app.py', 'admin_app.py', 'registration_app.py', 
                        'src/database.py', 'src/simple_face_recognition.py']
            files_status = []
            
            for file in app_files:
                if os.path.exists(file):
                    files_status.append(f"✅ {file}")
                else:
                    files_status.append(f"❌ {file}")
            
            # Create info dialog
            info_text = (f"🏢 ATTENDANCE SYSTEM - SYSTEM INFORMATION\n\n" +
                        f"🐍 Python Version: {python_version}\n" +
                        f"📂 Working Directory: {os.getcwd()}\n\n" +
                        f"📦 Required Modules:\n" +
                        "\n".join(modules_status) + "\n\n" +
                        f"📄 Application Files:\n" +
                        "\n".join(files_status) + "\n\n" +
                        f"💾 Database: SQLite (embedded)\n" +
                        f"👁️ Face Recognition: OpenCV Haar Cascades\n" +
                        f"🖥️ GUI Framework: Tkinter\n\n" +
                        f"📞 Support: Check documentation for troubleshooting")
            
            messagebox.showinfo("System Information", info_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to gather system information: {str(e)}")
    
    def exit_launcher(self):
        """Exit the launcher application"""
        if messagebox.askyesno("Exit Launcher", 
                              "Are you sure you want to exit the Attendance System Launcher?"):
            self.root.quit()

def main():
    # Create root window
    root = tk.Tk()
    
    # Hide root window initially
    root.withdraw()
    
    # Create and show launcher
    launcher = AttendanceLauncher(root)
    
    # Show the window
    root.deiconify()
    
    # Start the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
