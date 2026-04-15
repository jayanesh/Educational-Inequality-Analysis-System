@echo off
title School Dropout Analysis System
echo --------------------------------------------------
echo [1/3] Applying Required Database Migrations...
python manage.py migrate
echo.
echo [2/3] Ingesting UDISE+ Dataset into MongoDB...
python load_data.py
echo.
echo [3/3] Starting Django Development Server...
echo The dashboard will be available at http://127.0.0.1:8000/
python manage.py runserver
pause
