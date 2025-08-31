"""
Facial Recognition Attendance System - User Application
Author: Uzman Jawaid
Description: Simple interface for employees to mark attendance using face recognition
Version: 2.0
Date: August 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime, date
from src.database import Database
from src.simple_face_recognition import SimpleFaceRecognizer

class UserAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System - User")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db = Database()
        self.face_recognizer = SimpleFaceRecognizer()
        
        # Camera variables
        self.cap = None
        self.camera_running = False
        self.video_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_label = tk.Label(self.root, text="📸 ATTENDANCE SYSTEM - USER", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Camera section
        camera_frame = ttk.LabelFrame(main_frame, text="Camera View - Face Recognition")
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.camera_label = tk.Label(camera_frame, text="Click 'Start Camera' to begin attendance marking", 
                                   bg='gray', width=80, height=25)
        self.camera_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Camera controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        self.start_camera_btn = ttk.Button(controls_frame, text="🎥 Start Camera", 
                                         command=self.start_camera, style='Accent.TButton')
        self.start_camera_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_camera_btn = ttk.Button(controls_frame, text="⏹️ Stop Camera", 
                                        command=self.stop_camera, state=tk.DISABLED)
        self.stop_camera_btn.pack(side=tk.LEFT, padx=10)
        
        # Quick status section
        status_frame = ttk.LabelFrame(main_frame, text="Today's Status")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_text = tk.Text(status_frame, height=8, width=80, font=('Courier', 10))
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Refresh button
        refresh_btn = ttk.Button(main_frame, text="🔄 Refresh Status", 
                               command=self.refresh_status)
        refresh_btn.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Click 'Start Camera' to begin")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load initial status
        self.refresh_status()
    
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
        
        self.status_var.set("Camera active - Looking for faces...")
    
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
                    status, time_in, time_out = self.get_employee_status(name)
                
                # Draw rectangle around face with status colors
                if name == "Unknown":
                    color = (0, 0, 255)  # Red for unknown
                elif status == "checked_in":
                    color = (0, 255, 255)  # Yellow for checked in
                elif status == "checked_out":
                    color = (0, 255, 0)  # Green for checked out
                else:
                    color = (255, 0, 0)  # Blue for not present today
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw status label
                if name != "Unknown":
                    if status == "checked_in":
                        label = f"{name} - CHECKED IN ({time_in})"
                    elif status == "checked_out":
                        label = f"{name} - CHECKED OUT ({time_out})"
                    else:
                        label = f"{name} - Ready to check in"
                else:
                    label = "Unknown Person"
                
                # Draw label background and text
                (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (left, bottom + 5), (left + label_width + 10, bottom + label_height + 15), color, cv2.FILLED)
                cv2.putText(frame, label, (left + 5, bottom + label_height + 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Mark attendance for known faces with high confidence
                if name != "Unknown" and confidence > 0.5:  # Lowered threshold for better detection
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
    
    def mark_attendance_smart(self, name, current_status):
        """Smart attendance marking with alerts"""
        # Simple throttling mechanism
        current_time = datetime.now()
        
        if hasattr(self, '_last_recognition'):
            if name in self._last_recognition:
                time_diff = (current_time - self._last_recognition[name]).total_seconds()
                if time_diff < 15:  # 15 second cooldown to prevent spam
                    return
        else:
            self._last_recognition = {}
        
        self._last_recognition[name] = current_time
        
        try:
            if current_status == "not_present":
                # User detected - Mark as present with alert
                success = self.db.mark_attendance(name)
                if success:
                    # Show success alert
                    self.root.after(0, lambda: self.show_attendance_alert(
                        "✅ CHECK-IN SUCCESSFUL", 
                        f"Welcome {name}!\nTime IN marked successfully.\n\nTime: {datetime.now().strftime('%H:%M:%S')}"
                    ))
                    self.root.after(0, lambda: self.status_var.set(f"✅ {name} CHECKED IN at {datetime.now().strftime('%H:%M:%S')}"))
                    self.root.after(0, self.refresh_status)
                else:
                    # Show error alert
                    self.root.after(0, lambda: self.show_attendance_alert(
                        "❌ CHECK-IN FAILED", 
                        f"Failed to mark attendance for {name}.\nPlease try again or use manual check-in."
                    ))
                    
            elif current_status == "checked_in":
                # User is already present - Mark timeout with alert
                success = self.db.mark_time_out(name)
                if success:
                    # Show timeout success alert
                    self.root.after(0, lambda: self.show_attendance_alert(
                        "🏠 TIME-OUT SUCCESSFUL", 
                        f"Goodbye {name}!\nTime OUT marked successfully.\n\nTime: {datetime.now().strftime('%H:%M:%S')}"
                    ))
                    self.root.after(0, lambda: self.status_var.set(f"🏠 {name} TIMED OUT at {datetime.now().strftime('%H:%M:%S')}"))
                    self.root.after(0, self.refresh_status)
                else:
                    # Show timeout error alert
                    self.root.after(0, lambda: self.show_attendance_alert(
                        "❌ TIME-OUT FAILED", 
                        f"Failed to mark time-out for {name}.\nPlease try again or use manual time-out."
                    ))
                    
            elif current_status == "checked_out":
                # User already timed out today
                self.root.after(0, lambda: self.show_attendance_alert(
                    "ℹ️ ALREADY COMPLETED", 
                    f"{name}, you have already\ncompleted your attendance for today.\n\nCheck-in: Available\nTime-out: Already done"
                ))
                self.root.after(0, lambda: self.status_var.set(f"ℹ️ {name} already completed attendance for today"))
                
        except Exception as e:
            print(f"Error in attendance marking: {e}")
            # Show general error alert
            self.root.after(0, lambda: self.show_attendance_alert(
                "❌ SYSTEM ERROR", 
                f"An error occurred while processing\nattendance for {name}.\n\nError: {str(e)}"
            ))
    
    def get_employee_status(self, name):
        """Get current status of an employee"""
        status, time_in, time_out = self.db.get_employee_status(name)
        return status, time_in, time_out
    
    def refresh_status(self):
        """Refresh today's attendance status"""
        self.status_text.delete(1.0, tk.END)
        
        today = date.today().strftime("%Y-%m-%d")
        records = self.db.get_attendance_records(date=today)
        
        self.status_text.insert(tk.END, f"📅 TODAY'S ATTENDANCE - {today}\n")
        self.status_text.insert(tk.END, "=" * 60 + "\n\n")
        
        if records:
            checked_in_count = 0
            checked_out_count = 0
            
            for record in records:
                name = record[2]
                time_in = record[4]
                time_out = record[5] if record[5] else "Still checked in"
                
                if record[5]:  # Has time out
                    status_icon = "🟢"
                    checked_out_count += 1
                else:  # Still checked in
                    status_icon = "🟡"
                    checked_in_count += 1
                
                self.status_text.insert(tk.END, f"{status_icon} {name:<20} IN: {time_in:<10} OUT: {time_out}\n")
            
            self.status_text.insert(tk.END, f"\n📊 SUMMARY:\n")
            self.status_text.insert(tk.END, f"   Currently at work: {checked_in_count}\n")
            self.status_text.insert(tk.END, f"   Completed day: {checked_out_count}\n")
            self.status_text.insert(tk.END, f"   Total today: {len(records)}\n")
        else:
            self.status_text.insert(tk.END, "No attendance records for today.\n\n")
            self.status_text.insert(tk.END, "Start the camera to begin marking attendance!")
        
        # Auto-scroll to top
        self.status_text.see(1.0)
    
    def show_attendance_alert(self, title, message):
        """Show attendance alert dialog with sound"""
        try:
            # Create a custom dialog window
            alert_window = tk.Toplevel(self.root)
            alert_window.title(title)
            alert_window.geometry("400x200")
            alert_window.configure(bg='white')
            alert_window.resizable(False, False)
            
            # Center the alert window
            alert_window.transient(self.root)
            alert_window.grab_set()
            
            # Position relative to parent window
            self.root.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
            alert_window.geometry(f"400x200+{x}+{y}")
            
            # Title label with icon
            title_frame = tk.Frame(alert_window, bg='white')
            title_frame.pack(fill='x', pady=(20, 10))
            
            title_label = tk.Label(title_frame, 
                                 text=title,
                                 font=('Arial', 14, 'bold'),
                                 bg='white',
                                 fg='#2c3e50')
            title_label.pack()
            
            # Message label
            message_frame = tk.Frame(alert_window, bg='white')
            message_frame.pack(fill='both', expand=True, pady=10)
            
            message_label = tk.Label(message_frame, 
                                   text=message,
                                   font=('Arial', 11),
                                   bg='white',
                                   fg='#34495e',
                                   justify='center',
                                   wraplength=350)
            message_label.pack(expand=True)
            
            # OK button
            button_frame = tk.Frame(alert_window, bg='white')
            button_frame.pack(fill='x', pady=(0, 20))
            
            ok_button = tk.Button(button_frame, 
                                text="OK",
                                font=('Arial', 10, 'bold'),
                                bg='#3498db',
                                fg='white',
                                relief='flat',
                                padx=30, pady=8,
                                cursor='hand2',
                                command=alert_window.destroy)
            ok_button.pack()
            
            # Auto-close after 5 seconds
            alert_window.after(5000, alert_window.destroy)
            
            # Make system beep for attention
            alert_window.bell()
            
        except Exception as e:
            print(f"Error showing alert: {e}")
            # Fallback to simple messagebox
            messagebox.showinfo(title, message)
    
    def on_closing(self):
        """Handle application closing"""
        if self.camera_running:
            self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    
    # Apply modern style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = UserAttendanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
