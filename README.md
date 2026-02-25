# OMNA Student Management System

A comprehensive Python-based desktop application for managing student records, attendance, and payments.

## Features

- **Student Management**: Add, view, update, and delete student records.
- **Search Functionality**: Quickly find students by Name (First/Last) or Student ID.
- **Data Filtering**: Easily filter the student list by academic level (e.g., 1ere TSDI, 2eme TSGE).
- **Attendance Tracker**: 
  - Record daily attendance with status (Present, Absent, Late).
  - Add optional notes for each entry.
  - View complete attendance history in a dedicated tab.
- **Payment Tracker**: 
  - Record payments with amount, date, and description.
  - View complete payment history in a dedicated tab.
- **Student Details View**: A tabbed interface to seamlessly switch between Profile, Attendance History, and Payment History.
- **Dashboard**: Quick overview of total student count and system status.
- **Modern UI**: Clean and user-friendly interface built with Tkinter and ttk.

## Project Structure

- `student_manager.py`: Main application entry point containing the GUI logic and event handling.
- `model.py`: Core data handling logic (CRUD operations for students, attendance, payments).
- `students.json`: JSON database file storing all student records, attendance logs, and payment history.
- `verify_app.py`: Utility script to verify the application loads correctly.

## Requirements

- Python 3.x
- Tkinter (usually included with Python standard library)

## Installation & Setup

1. **Clone or Download** the project files to your local machine.
2. Ensure you have **Python 3.x** installed.
3. No external dependencies are required as it uses standard libraries.

## Usage

1. **Run the Application**:
   Open a terminal in the project directory and run:
   ```bash
   python student_manager.py
   ```

2. **Navigate the Sidebar**:
   - **Dashboard**: Overview.
   - **All Students**: View the list of all students. Use the **Filter by Level** dropdown to narrow down the list.
   - **Add Student**: Fill in the form to register a new student.
   - **Search Student**: Enter a name or ID to find specific records.
   - **Attendance**: Select a student to view their history or add a new attendance record.
   - **Payments**: Select a student to view their history or add a new payment record.

3. **Manage Student Details**:
   - Double-click any student in the list to open their details.
   - Use the **tabs** at the top (Profile, Attendance History, Payment History) to view specific information.
   - Use the **Record Attendance** and **Record Payment** buttons for quick actions.

## Data Storage

All data is persistently stored in `students.json`. This file is automatically updated as you use the application.
**Note**: Avoid manually editing `students.json` to prevent data corruption.

## Future Improvements

- Export data to CSV/Excel.
- Authentication for admin access.
- Advanced reporting and analytics (e.g., monthly attendance reports).
