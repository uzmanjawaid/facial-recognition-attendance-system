#!/usr/bin/env python3
"""
Demo script for the Facial Recognition Attendance System

This script demonstrates the basic functionality of the system
without requiring a GUI interface.
"""

import os
import sys
import cv2
from datetime import datetime

# Add src to path
sys.path.append('src')

from database import Database
from simple_face_recognition import SimpleFaceRecognizer

def demo_system():
    """Demonstrate the attendance system functionality"""
    print("="*60)
    print("  Facial Recognition Attendance System - Demo")
    print("="*60)
    
    # Initialize components
    db = Database()
    recognizer = SimpleFaceRecognizer()
    
    print("\n1. Database Initialization")
    print("   - Database created/loaded successfully")
    print("   - Face recognition system initialized")
    
    # Add some demo employees
    print("\n2. Adding Demo Employees")
    demo_employees = [
        ("John Doe", "john@company.com", "123-456-7890", "Engineering"),
        ("Jane Smith", "jane@company.com", "123-456-7891", "HR"),
        ("Bob Johnson", "bob@company.com", "123-456-7892", "Marketing")
    ]
    
    for name, email, phone, dept in demo_employees:
        employee_id = db.add_employee(name, email, phone, dept)
        if employee_id:
            print(f"   ✓ Added employee: {name}")
        else:
            print(f"   - Employee {name} already exists")
    
    # Show employees
    print("\n3. Current Employees")
    employees = db.get_all_employees()
    for emp in employees:
        print(f"   - ID: {emp[0]}, Name: {emp[1]}, Email: {emp[2]}, Dept: {emp[4]}")
    
    # Demo attendance marking
    print("\n4. Marking Demo Attendance")
    demo_attendance = ["John Doe", "Jane Smith"]
    for name in demo_attendance:
        success = db.mark_attendance(name)
        if success:
            print(f"   ✓ Marked attendance for {name}")
    
    # Show today's attendance
    print("\n5. Today's Attendance Records")
    today = datetime.now().strftime("%Y-%m-%d")
    records = db.get_attendance_records(date=today)
    
    if records:
        print("   Records found:")
        for record in records:
            print(f"   - {record[2]} | In: {record[4]} | Out: {record[5] or 'Not marked'}")
    else:
        print("   No attendance records for today")
    
    # Test camera (optional)
    print("\n6. Camera Test (Optional)")
    response = input("   Would you like to test camera detection? (y/n): ").lower()
    
    if response == 'y':
        test_camera(recognizer)
    
    print("\n" + "="*60)
    print("  Demo completed successfully!")
    print("  Run 'python main.py' to start the GUI application")
    print("="*60)

def test_camera(recognizer):
    """Test camera face detection"""
    print("   Starting camera test...")
    print("   Press 'q' to quit camera test")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("   ❌ Could not open camera")
        return
    
    print("   ✓ Camera opened successfully")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Test face detection every 30 frames
        if frame_count % 30 == 0:
            recognized_faces = recognizer.recognize_faces_in_frame(frame)
            print(f"   Detected {len(recognized_faces)} face(s)")
        
        # Show frame
        cv2.imshow('Camera Test - Press Q to quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("   Camera test completed")

if __name__ == "__main__":
    try:
        demo_system()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("Please check that all dependencies are installed correctly")
