#!/usr/bin/env python3
"""
Database and Pictures Cleanup Utility

This script safely clears all attendance data, employee records, 
face templates, and stored images from the system.
"""

import os
import shutil
import sqlite3
from datetime import datetime

def clear_database():
    """Clear all data from the database"""
    db_path = "data/attendance.db"
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Clear attendance records
            cursor.execute("DELETE FROM attendance")
            print("✓ Cleared attendance records")
            
            # Clear employee records
            cursor.execute("DELETE FROM employees")
            print("✓ Cleared employee records")
            
            # Reset auto-increment counters
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='attendance'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")
            print("✓ Reset ID counters")
            
            conn.commit()
            conn.close()
            
            print(f"✓ Database cleared successfully: {db_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            return False
    else:
        print("ℹ️  Database file not found, nothing to clear")
        return True

def clear_face_pictures():
    """Clear all stored face pictures"""
    faces_dir = "data/faces"
    
    if os.path.exists(faces_dir):
        try:
            # Remove all subdirectories and files
            for item in os.listdir(faces_dir):
                item_path = os.path.join(faces_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"✓ Removed face directory: {item}")
                else:
                    os.remove(item_path)
                    print(f"✓ Removed face file: {item}")
            
            print(f"✓ Face pictures cleared successfully: {faces_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing face pictures: {e}")
            return False
    else:
        print("ℹ️  Face pictures directory not found, nothing to clear")
        return True

def clear_face_templates():
    """Clear face recognition templates"""
    template_path = "models/face_encodings.pkl"
    simple_template_path = "models/face_templates.pkl"
    
    cleared_files = []
    
    for file_path in [template_path, simple_template_path]:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                cleared_files.append(file_path)
                print(f"✓ Removed face template: {file_path}")
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
                return False
    
    if cleared_files:
        print("✓ Face templates cleared successfully")
    else:
        print("ℹ️  No face template files found, nothing to clear")
    
    return True

def create_backup():
    """Create a backup before clearing (optional)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    try:
        if os.path.exists("data") or os.path.exists("models"):
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup data directory
            if os.path.exists("data"):
                shutil.copytree("data", f"{backup_dir}/data")
                print(f"✓ Backed up data to {backup_dir}/data")
            
            # Backup models directory
            if os.path.exists("models"):
                shutil.copytree("models", f"{backup_dir}/models")
                print(f"✓ Backed up models to {backup_dir}/models")
            
            print(f"✓ Backup created in directory: {backup_dir}")
            return backup_dir
        else:
            print("ℹ️  No data to backup")
            return None
            
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def main():
    """Main cleanup function with user confirmation"""
    print("=" * 60)
    print("  FACIAL RECOGNITION ATTENDANCE SYSTEM")
    print("  DATABASE AND PICTURES CLEANUP UTILITY")
    print("=" * 60)
    print()
    
    print("This will permanently delete:")
    print("• All employee records")
    print("• All attendance records") 
    print("• All face pictures")
    print("• All face recognition templates")
    print()
    
    # Ask for confirmation
    response = input("Are you sure you want to continue? (type 'YES' to confirm): ")
    
    if response != "YES":
        print("❌ Operation cancelled")
        return
    
    # Ask about backup
    backup_response = input("Create backup before clearing? (y/n): ").lower()
    backup_dir = None
    
    if backup_response == 'y':
        print("\n📦 Creating backup...")
        backup_dir = create_backup()
        if not backup_dir:
            proceed = input("Backup failed. Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                print("❌ Operation cancelled")
                return
    
    print("\n🗑️  Starting cleanup...")
    
    # Clear database
    print("\n1. Clearing database...")
    db_success = clear_database()
    
    # Clear face pictures
    print("\n2. Clearing face pictures...")
    pics_success = clear_face_pictures()
    
    # Clear face templates
    print("\n3. Clearing face templates...")
    templates_success = clear_face_templates()
    
    # Summary
    print("\n" + "=" * 60)
    if db_success and pics_success and templates_success:
        print("✅ CLEANUP COMPLETED SUCCESSFULLY!")
        print()
        print("All data has been cleared from the system.")
        print("The system is now reset to initial state.")
        if backup_dir:
            print(f"📦 Backup saved in: {backup_dir}")
    else:
        print("⚠️  CLEANUP COMPLETED WITH SOME ERRORS")
        print("Please check the error messages above.")
    
    print("=" * 60)
    print()
    print("You can now:")
    print("• Run the application: python main.py")
    print("• Register new employees")
    print("• Start fresh attendance tracking")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
