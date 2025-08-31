# 🎯 Facial Recognition Attendance System

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0%2B-green.svg)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Uzman%20Jawaid-red.svg)](https://github.com/uzman-jawaid)

> A comprehensive Python-based attendance management system with facial recognition technology, featuring role-based applications and automated attendance tracking.

![Attendance System Demo](https://via.placeholder.com/800x400/2c3e50/ffffff?text=Facial+Recognition+Attendance+System)

## 🚀 Features

### 🎯 **Core Functionality**
- **Real-time Face Recognition**: Automatic attendance marking using webcam
- **Smart Attendance Management**: Auto check-in and time-out with visual alerts
- **Role-based Applications**: Separate interfaces for different user types
- **Professional GUI**: Modern Tkinter-based interfaces with enhanced UX
- **Database Integration**: SQLite database for reliable data storage

### 📱 **Three Specialized Applications**

#### 1. 👤 **User Application** (`user_app.py`)
**For Employees**
- ✅ Simple attendance marking interface
- 📷 Real-time camera view (800x600)
- 🚨 Visual and audio alerts for check-in/time-out
- 📊 Personal attendance status display
- 🔄 Automatic recognition and marking

#### 2. 👨‍💼 **Admin Application** (`admin_app.py`)
**For Administrators**
- 📈 Comprehensive attendance records management
- 📋 Advanced filtering by date and employee
- 📊 Real-time statistics and analytics
- 💾 CSV export for reporting
- 👥 Employee management system

#### 3. 📝 **Registration Application** (`registration_app.py`)
**For HR/Setup Personnel**
- 👤 New employee registration
- 📸 Face capture with camera (5 photos)
- 📁 Image upload alternative
- 🗄️ Employee database management
- 📋 Registration status monitoring

### 🚀 **Central Launcher** (`launcher.py`)
- 🎮 Beautiful application selector
- ℹ️ System information display
- 🔧 Quick access to all modules
- 💻 Professional dashboard interface

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [⚙️ Installation](#️-installation)
- [📖 Usage Guide](#-usage-guide)
- [🏗️ Project Structure](#️-project-structure)
- [🎨 Screenshots](#-screenshots)
- [🔧 Technical Details](#-technical-details)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🚀 Quick Start

### **Launch the Application**
```bash
# Clone the repository
git clone https://github.com/uzman-jawaid/facial-recognition-attendance-system.git
cd facial-recognition-attendance-system

# Install dependencies
pip install opencv-python pillow

# Start the system
python launcher.py
```

### **First-Time Setup**
1. **Launch** the application launcher
2. **Open Registration App** to add employees
3. **Capture face photos** for each employee
4. **Open User App** to start marking attendance

## ⚙️ Installation

### **Prerequisites**
- 🐍 **Python 3.7+**
- 📷 **Webcam/Camera**
- 💻 **Windows 10+, macOS 10.14+, or Linux**

### **Dependencies**
```bash
pip install opencv-python pillow
```

### **System Requirements**
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Camera**: USB webcam or built-in camera
- **Screen**: 1024x768 minimum resolution

## 📖 Usage Guide

### 🎮 **Application Launcher**
Start the central hub to access all applications:
```bash
python launcher.py
```

### 👤 **User Application - Daily Attendance**
For employees to mark their attendance:

1. **Launch**: Click "User Application" from launcher
2. **Start Camera**: Click "Start Camera" button
3. **Position**: Stand in front of camera
4. **Automatic Recognition**: System detects and marks attendance
5. **Alerts**: Visual notifications for check-in/time-out

**Features:**
- 🎯 Automatic check-in when first detected
- 🏠 Automatic time-out when detected again
- 🚨 Visual alerts with sound notifications
- 📊 Real-time attendance status display

### 👨‍💼 **Admin Application - Management**
For administrators to manage the system:

1. **Launch**: Click "Admin Application" from launcher
2. **View Records**: Browse all attendance data
3. **Filter Data**: By date range or employee
4. **Generate Reports**: Export to CSV format
5. **Manage Employees**: Add/remove employee records

### 📝 **Registration Application - Setup**
For HR to register new employees:

1. **Launch**: Click "Registration Application" from launcher
2. **Enter Details**: Fill employee information
3. **Capture Face**: Use camera to take 5 photos
4. **Register**: Save employee and face data
5. **Monitor**: View registration statistics

## 🏗️ Project Structure

```
facial-recognition-attendance-system/
├── 📁 Root Applications
│   ├── launcher.py              # 🚀 Central launcher
│   ├── user_app.py             # 👤 User attendance app
│   ├── admin_app.py            # 👨‍💼 Admin management app
│   └── registration_app.py     # 📝 Employee registration app
├── 📁 src/                     # Core system modules
│   ├── database.py             # 🗄️ Database operations
│   └── simple_face_recognition.py  # 👁️ Face recognition
├── 📁 data/                    # Auto-generated data
│   ├── attendance.db           # 💾 SQLite database
│   └── known_faces/            # 📸 Face templates
├── 📁 docs/                    # Documentation
│   └── README.md               # 📖 This file
└── 📁 config/
    └── requirements.txt        # 📦 Dependencies
```

## 🎨 Screenshots

### 🎮 Application Launcher
![Launcher](https://via.placeholder.com/600x400/3498db/ffffff?text=Application+Launcher)

### 👤 User Application
![User App](https://via.placeholder.com/600x400/27ae60/ffffff?text=User+Attendance+Interface)

### 👨‍💼 Admin Panel
![Admin App](https://via.placeholder.com/600x400/e74c3c/ffffff?text=Admin+Management+Panel)

## 🔧 Technical Details

### **🧠 Face Recognition Technology**
- **Method**: OpenCV Haar Cascades with template matching
- **Accuracy**: Optimized for various lighting conditions
- **Performance**: Real-time processing at 30 FPS
- **Storage**: Local face templates for privacy

### **🗄️ Database Schema**

#### **Employees Table**
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT,
    phone TEXT,
    department TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Attendance Table**
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time_in TEXT,
    time_out TEXT,
    status TEXT DEFAULT 'Present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **🔄 System Workflow**
1. **Face Detection**: Haar Cascade detects faces in frame
2. **Feature Extraction**: Histogram comparison for recognition
3. **Database Query**: Check employee status
4. **Smart Logic**: Determine check-in vs time-out
5. **Alert System**: Visual and audio notifications
6. **Data Storage**: Update attendance records

## 🐛 Troubleshooting

### **Common Issues**

#### 📷 **Camera Problems**
```bash
# Check camera permissions
# Windows: Settings > Privacy > Camera
# Try different camera index
# Close other camera applications
```

#### 🎭 **Face Recognition Issues**
```bash
# Ensure good lighting
# Re-register face photos
# Clean camera lens
# Check face photo quality
```

#### 🐍 **Python/Installation Problems**
```bash
# Verify Python version
python --version

# Reinstall dependencies
pip uninstall opencv-python pillow
pip install opencv-python pillow

# Check system compatibility
python -c "import cv2; print('OpenCV:', cv2.__version__)"
```

#### 🗄️ **Database Issues**
```bash
# Reset database (caution: deletes all data)
rm data/attendance.db

# Check database permissions
ls -la data/
```

### **Performance Optimization**

#### 🚀 **Speed Improvements**
- Close unnecessary applications
- Ensure good lighting
- Use dedicated USB camera
- Regular system updates

#### 🎯 **Accuracy Enhancements**
- Register multiple face angles
- Consistent lighting during registration
- High-quality camera resolution
- Regular face template updates

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### **🔀 Fork & Clone**
```bash
git clone https://github.com/your-username/facial-recognition-attendance-system.git
cd facial-recognition-attendance-system
```

### **🌿 Create Branch**
```bash
git checkout -b feature/your-feature-name
```

### **✅ Make Changes**
- Follow existing code style
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation if needed

### **📤 Submit PR**
```bash
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### **🐛 Bug Reports**
Please include:
- System information
- Python version
- Error messages
- Steps to reproduce

## 🎖️ Author

**Uzman Jawaid**
- 📧 Email: [uzman.jawaid@example.com]
- 🐙 GitHub: [@uzman-jawaid](https://github.com/uzman-jawaid)
- 💼 LinkedIn: [Uzman Jawaid](https://linkedin.com/in/uzman-jawaid)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Uzman Jawaid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- **OpenCV Team** - Computer vision library
- **Python Community** - Programming language and ecosystem
- **Tkinter** - GUI framework
- **SQLite** - Embedded database system

## 🔮 Future Enhancements

- [ ] 🌐 Web-based interface
- [ ] 📧 Email notifications
- [ ] 📱 Mobile app integration
- [ ] ☁️ Cloud database support
- [ ] 🤖 Advanced ML models
- [ ] 📊 Analytics dashboard
- [ ] 🔒 Enhanced security features
- [ ] 🌍 Multi-language support

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/uzman-jawaid/facial-recognition-attendance-system?style=social)
![GitHub forks](https://img.shields.io/github/forks/uzman-jawaid/facial-recognition-attendance-system?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/uzman-jawaid/facial-recognition-attendance-system?style=social)

---

<div align="center">

**⭐ Star this repository if it helped you! ⭐**

Made with ❤️ by [Uzman Jawaid](https://github.com/uzman-jawaid)

</div>
