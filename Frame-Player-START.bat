@echo off
echo Checking for virtual environment...

IF NOT EXIST venv\ (
    echo Creating virtual environment...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Please ensure Python is installed correctly.
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

echo Activating virtual environment...
call venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install --upgrade opencv-python Pillow
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Dependencies are up to date.

echo frame_player.py running...
python frame_player.py
