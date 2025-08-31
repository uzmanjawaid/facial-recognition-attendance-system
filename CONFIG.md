# Project Configuration

## File Structure
```
facial-recognition-attendance/
├── main.py                           # Main application entry point
├── demo.py                           # Demo script for testing
├── requirements.txt                  # Python dependencies
├── setup.bat                         # Windows setup script
├── README.md                         # Comprehensive documentation
├── .vscode/
│   └── tasks.json                    # VS Code tasks configuration
├── .github/
│   └── copilot-instructions.md       # Copilot workspace instructions
├── src/
│   ├── main_gui.py                   # Main GUI application
│   ├── database.py                   # Database operations
│   ├── face_recognition_system.py    # Advanced face recognition (requires additional setup)
│   └── simple_face_recognition.py    # OpenCV-based face detection
├── data/
│   ├── attendance.db                 # SQLite database (auto-generated)
│   └── faces/                        # Face image storage
└── models/
    └── face_templates.pkl            # Face templates storage (auto-generated)
```

## Quick Start
1. **Run Demo**: `python demo.py`
2. **Start GUI**: `python main.py`
3. **VS Code**: Use Ctrl+Shift+P → "Tasks: Run Task" → "Run Attendance System"

## System Architecture

### Database Layer (`database.py`)
- SQLite database with employees and attendance tables
- CRUD operations for employee management
- Attendance tracking with time-in/time-out
- Reporting and filtering capabilities

### Face Recognition Layer
- **Simple Version** (`simple_face_recognition.py`): Uses OpenCV Haar Cascades
- **Advanced Version** (`face_recognition_system.py`): Uses face_recognition library
- Template storage and matching algorithms
- Camera integration for live recognition

### GUI Layer (`main_gui.py`)
- **Attendance Tab**: Real-time camera feed with face recognition
- **Registration Tab**: Employee registration with face capture
- **Admin Panel**: Attendance records management and reporting
- Export functionality and statistics

## Configuration Options

### Camera Settings
- Default camera index: 0 (change in code if needed)
- Face detection threshold: Adjustable in recognition classes
- Frame processing: Optimized for real-time performance

### Recognition Settings
- Confidence threshold: 0.6 (adjustable)
- Template matching method: Histogram correlation
- Face capture: 5 photos per person (configurable)

### Database Settings
- Default location: `data/attendance.db`
- Automatic backup recommended for production use
- Schema supports future extensions

## Upgrade Path

To upgrade to advanced face recognition:
1. Install required packages: `pip install face-recognition dlib cmake`
2. Update imports in `main_gui.py` to use `FaceRecognizer` instead of `SimpleFaceRecognizer`
3. The advanced system provides higher accuracy and better performance

## Troubleshooting

### Common Issues
1. **Camera Access**: Ensure no other applications are using the camera
2. **Face Detection**: Ensure good lighting and clear face visibility
3. **Performance**: Reduce camera resolution if needed

### Windows-Specific
- Some camera warnings are normal with Windows Media Foundation
- For better camera support, install additional camera drivers if needed
