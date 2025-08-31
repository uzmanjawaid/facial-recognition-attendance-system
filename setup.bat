@echo off
echo ================================================
echo  Facial Recognition Attendance System Setup
echo ================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take several minutes...
echo.

pip install opencv-python==4.8.1.78
if %errorlevel% neq 0 (
    echo ERROR: Failed to install opencv-python
    pause
    exit /b 1
)

pip install pillow==10.0.1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install pillow
    pause
    exit /b 1
)

pip install numpy==1.24.3
if %errorlevel% neq 0 (
    echo ERROR: Failed to install numpy
    pause
    exit /b 1
)

echo.
echo Installing face recognition dependencies...
echo This step may take longer and require Visual C++ Build Tools
echo.

pip install cmake==3.27.4.1
pip install dlib==19.24.2
if %errorlevel% neq 0 (
    echo WARNING: Failed to install dlib
    echo Trying alternative installation method...
    pip install dlib-binary
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dlib
        echo Please install Microsoft Visual C++ Build Tools
        echo Or try: conda install -c conda-forge dlib
        pause
        exit /b 1
    )
)

pip install face-recognition==1.3.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to install face-recognition
    pause
    exit /b 1
)

echo.
echo ================================================
echo  Installation Complete!
echo ================================================
echo.
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "data\faces" mkdir data\faces
if not exist "models" mkdir models

echo.
echo Setup completed successfully!
echo.
echo To run the application:
echo 1. Open command prompt in this directory
echo 2. Run: python main.py
echo.
echo For troubleshooting, check README.md
echo.
pause
