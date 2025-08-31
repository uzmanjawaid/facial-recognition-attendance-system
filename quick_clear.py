#!/usr/bin/env python3
"""
Quick Database and Pictures Cleanup Script
Automatically clears all data without prompts.
"""

import os
import shutil
import sqlite3
from datetime import datetime

def clear_all_data():
    """Clear all data from the system"""
    print("🗑️  Starting automatic cleanup...")
    
    # Create backup first
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
    except Exception as e:
        print(f"Warning: Backup failed: {e}")
    
    # Clear database
    db_path = "data/attendance.db"
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM attendance")
            cursor.execute("DELETE FROM employees") 
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='attendance'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")
            
            conn.commit()
            conn.close()
            print("✓ Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {e}")
    
    # Clear face pictures
    faces_dir = "data/faces"
    if os.path.exists(faces_dir):
        try:
            for item in os.listdir(faces_dir):
                item_path = os.path.join(faces_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            print("✓ Face pictures cleared")
        except Exception as e:
            print(f"Error clearing pictures: {e}")
    
    # Clear face templates
    for template_file in ["models/face_encodings.pkl", "models/face_templates.pkl"]:
        if os.path.exists(template_file):
            try:
                os.remove(template_file)
                print(f"✓ Removed {template_file}")
            except Exception as e:
                print(f"Error removing {template_file}: {e}")
    
    print("\n✅ CLEANUP COMPLETED!")
    print("All employee records, attendance data, pictures, and face templates have been cleared.")
    if 'backup_dir' in locals():
        print(f"📦 Backup created in: {backup_dir}")

if __name__ == "__main__":
    clear_all_data()
