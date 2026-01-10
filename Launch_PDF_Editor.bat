@echo off
REM PDF Editor Launcher
REM This batch file launches the PDF editor application

echo Starting PDF Editor...
python pdf_editor_complete.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Error launching PDF Editor!
    echo Make sure Python is installed and in your PATH.
    pause
)
