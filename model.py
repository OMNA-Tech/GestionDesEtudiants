import json
import os
from datetime import datetime

DATA_FILE = "students.json"

class StudentModel:
    def __init__(self):
        self.students = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.students, f, indent=4)

    def get_all_students(self):
        return self.students

    def add_student(self, student_data):
        # Generate a simple ID if not provided
        if "id" not in student_data or not student_data["id"]:
            student_data["id"] = f"S{len(self.students) + 1:04d}"
        
        # Initialize empty trackers
        student_data["attendance"] = []
        student_data["payments"] = []
        
        self.students.append(student_data)
        self.save_data()
        return student_data["id"]

    def delete_student(self, student_id):
        initial_count = len(self.students)
        self.students = [s for s in self.students if s.get("id") != student_id]
        if len(self.students) < initial_count:
            self.save_data()
            return True
        return False

    def update_student(self, student_id, updated_data):
        for student in self.students:
            if student.get("id") == student_id:
                student.update(updated_data)
                self.save_data()
                return True
        return False

    def search_students(self, query):
        query = query.lower()
        results = []
        for student in self.students:
            if (query in student.get("first_name", "").lower() or 
                query in student.get("last_name", "").lower() or 
                query in student.get("id", "").lower()):
                results.append(student)
        return results

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student.get("id") == student_id:
                return student
        return None

    def add_attendance(self, student_id, date, status, notes=""):
        student = self.get_student_by_id(student_id)
        if student:
            if "attendance" not in student:
                student["attendance"] = []
            
            record = {
                "date": date,
                "status": status,
                "notes": notes,
                "timestamp": datetime.now().isoformat()
            }
            student["attendance"].append(record)
            self.save_data()
            return True
        return False

    def add_payment(self, student_id, amount, date, description=""):
        student = self.get_student_by_id(student_id)
        if student:
            if "payments" not in student:
                student["payments"] = []
            
            record = {
                "date": date,
                "amount": amount,
                "description": description,
                "timestamp": datetime.now().isoformat()
            }
            student["payments"].append(record)
            self.save_data()
            return True
        return False
