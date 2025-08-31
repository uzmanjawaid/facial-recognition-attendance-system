"""
Facial Recognition Attendance System - Database Module
Author: Uzman Jawaid
Description: SQLite database operations for employee and attendance management
Version: 2.0
Date: August 2025
"""

import sqlite3
import os
from datetime import datetime, date

class Database:

class Database:
    def __init__(self, db_path="data/attendance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT,
                phone TEXT,
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time_in TEXT,
                time_out TEXT,
                status TEXT DEFAULT 'Present',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_employee(self, name, email="", phone="", department=""):
        """Add a new employee to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO employees (name, email, phone, department)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, department))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_employee_by_name(self, name):
        """Get employee information by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_all_employees(self):
        """Get all employees"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM employees ORDER BY name')
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def mark_attendance(self, name, status="Present"):
        """Mark attendance for an employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Check if attendance already exists for today
        cursor.execute('''
            SELECT * FROM attendance WHERE name = ? AND date = ?
        ''', (name, today))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update time_out if already checked in
            cursor.execute('''
                UPDATE attendance SET time_out = ? WHERE name = ? AND date = ?
            ''', (current_time, name, today))
        else:
            # Create new attendance record
            employee = self.get_employee_by_name(name)
            employee_id = employee[0] if employee else None
            
            cursor.execute('''
                INSERT INTO attendance (employee_id, name, date, time_in, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (employee_id, name, today, current_time, status))
        
        conn.commit()
        conn.close()
        
        return True
    
    def mark_time_out(self, name):
        """Explicitly mark time out for an employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Check if employee is checked in today
        cursor.execute('''
            SELECT * FROM attendance WHERE name = ? AND date = ? AND time_out IS NULL
        ''', (name, today))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update time_out
            cursor.execute('''
                UPDATE attendance SET time_out = ? WHERE name = ? AND date = ? AND time_out IS NULL
            ''', (current_time, name, today))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False  # Not checked in or already checked out
    
    def get_checked_in_employees(self):
        """Get list of employees currently checked in (no time_out)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute('''
            SELECT name, time_in FROM attendance 
            WHERE date = ? AND time_out IS NULL
            ORDER BY time_in
        ''', (today,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_employee_status(self, name):
        """Get current attendance status for an employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute('''
            SELECT time_in, time_out FROM attendance 
            WHERE name = ? AND date = ?
        ''', (name, today))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            time_in, time_out = result
            if time_out:
                return "checked_out", time_in, time_out
            else:
                return "checked_in", time_in, None
        else:
            return "not_present", None, None
    
    def get_attendance_records(self, date=None, name=None):
        """Get attendance records with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM attendance'
        params = []
        
        if date or name:
            query += ' WHERE'
            conditions = []
            
            if date:
                conditions.append(' date = ?')
                params.append(date)
            
            if name:
                conditions.append(' name = ?')
                params.append(name)
            
            query += ' AND'.join(conditions)
        
        query += ' ORDER BY date DESC, time_in DESC'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_attendance_summary(self, start_date=None, end_date=None):
        """Get attendance summary with statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT name, COUNT(*) as days_present,
                   MIN(date) as first_attendance,
                   MAX(date) as last_attendance
            FROM attendance
        '''
        params = []
        
        if start_date or end_date:
            query += ' WHERE'
            conditions = []
            
            if start_date:
                conditions.append(' date >= ?')
                params.append(start_date)
            
            if end_date:
                conditions.append(' date <= ?')
                params.append(end_date)
            
            query += ' AND'.join(conditions)
        
        query += ' GROUP BY name ORDER BY name'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
