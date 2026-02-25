import tkinter as tk
from tkinter import messagebox, ttk
from model import StudentModel
from datetime import datetime

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize Model
        self.model = StudentModel()
        self.current_student = None
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 10), padding=5)
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        
        self.allowed_levels = [
            "1ere TSDI", "2eme TSDI",
            "1ere TSGE", "2eme TSGE",
            "1ere TGI", "2eme TGI",
            "1ere OPS"
        ]
        
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#2c3e50", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="OMNA Center", bg="#2c3e50", fg="white", 
                 font=("Helvetica", 16, "bold")).pack(pady=20)
        
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👥 All Students", self.show_all_students),
            ("➕ Add Student", self.add_student_form),
            ("🔍 Search Student", self.search_student_form),
            ("📅 Attendance", self.attendance_tracker),
            ("💰 Payments", self.payment_tracker)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(self.sidebar, text=text, command=command, 
                           bg="#34495e", fg="white", activebackground="#2980b9", 
                           activeforeground="white", relief="flat", anchor="w", padx=20)
            btn.pack(fill="x", pady=2)
            
        tk.Label(self.sidebar, text="Filter by Level", bg="#2c3e50", fg="#bdc3c7", 
                 font=("Helvetica", 10, "bold")).pack(pady=(20, 10), padx=10, anchor="w")
        
        level_frame = tk.Frame(self.sidebar, bg="#2c3e50")
        level_frame.pack(fill="x", padx=10)
        
        self.level_var = tk.StringVar(value="All")
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, values=["All"] + self.allowed_levels, state="readonly")
        level_combo.pack(fill="x")
        level_combo.bind("<<ComboboxSelected>>", self.filter_students)

        # Main Content Area
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Welcome to OMNA Management System", 
                 font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=50)
        
        stats_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        stats_frame.pack(pady=20)
        
        total_students = len(self.model.students)
        tk.Label(stats_frame, text=f"Total Students: {total_students}", 
                 font=("Helvetica", 18), bg="white", padx=20, pady=20, relief="raised").pack(side="left", padx=20)

    def show_all_students(self, students=None, title="Student List", on_click=None):
        self.clear_main_frame()
        tk.Label(self.main_frame, text=title, font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(pady=(0, 20), anchor="w")
        
        # Table
        columns = ("id", "first_name", "last_name", "level", "phone")
        tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        tree.heading("id", text="ID")
        tree.heading("first_name", text="First Name")
        tree.heading("last_name", text="Last Name")
        tree.heading("level", text="Level")
        tree.heading("phone", text="Phone")
        
        tree.column("id", width=80)
        tree.column("first_name", width=120)
        tree.column("last_name", width=120)
        tree.column("level", width=100)
        tree.column("phone", width=100)
        
        tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        data = students if students else self.model.students
        for student in data:
            tree.insert("", "end", values=(
                student.get("id", ""),
                student.get("first_name", ""),
                student.get("last_name", ""),
                student.get("level", ""),
                student.get("phone", "")
            ))
            
        def default_click(event):
            selection = tree.selection()
            if not selection: return
            item = selection[0]
            values = tree.item(item, "values")
            student_id = values[0]
            self.show_student_details(student_id)
            
        # If a custom handler is provided, we wrap it to pass the tree so it can get selection
        if on_click:
            def wrapped_click(event):
                selection = tree.selection()
                if not selection: return
                item = selection[0]
                values = tree.item(item, "values")
                on_click(values[0])
            tree.bind("<Double-1>", wrapped_click)
        else:
            tree.bind("<Double-1>", default_click)

    def filter_students(self, event=None):
        level = self.level_var.get()
        if level == "All":
            self.show_all_students()
        else:
            filtered = [s for s in self.model.students if s.get("level") == level]
            self.show_all_students(filtered, title=f"Students in {level}")

    def add_student_form(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Add New Student", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(pady=(0, 20), anchor="w")
        
        form_frame = tk.Frame(self.main_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)
        
        fields = ["First Name", "Last Name", "DOB", "Gender", "Address", "Phone", "Reg Date"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field, bg="white", font=("Helvetica", 10, "bold")).grid(row=i, column=0, sticky="e", pady=10, padx=10)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.entries[field.lower().replace(" ", "_")] = entry
            
        tk.Label(form_frame, text="Level", bg="white", font=("Helvetica", 10, "bold")).grid(row=len(fields), column=0, sticky="e", pady=10, padx=10)
        level_combo = ttk.Combobox(form_frame, values=self.allowed_levels, state="readonly", width=28)
        level_combo.grid(row=len(fields), column=1, pady=10, padx=10)
        self.entries["level"] = level_combo
        
        submit_btn = tk.Button(form_frame, text="Save Student", command=self.save_student, bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"))
        submit_btn.grid(row=len(fields)+1, column=1, pady=20, sticky="e")

    def save_student(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        
        if not data["first_name"] or not data["last_name"]:
            messagebox.showerror("Error", "First Name and Last Name are required!")
            return
            
        self.model.add_student(data)
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_all_students()

    def search_student_form(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Search Student", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(pady=(0, 20), anchor="w")
        
        search_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search by Name or ID:", bg="#ecf0f1").pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=10)
        
        tk.Button(search_frame, text="Search", command=self.perform_search, bg="#3498db", fg="white").pack(side="left", padx=10)
        
        self.results_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        self.results_frame.pack(fill="both", expand=True)

    def perform_search(self):
        query = self.search_var.get()
        results = self.model.search_students(query)
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not results:
            tk.Label(self.results_frame, text="No students found.", bg="#ecf0f1", fg="red").pack(pady=20)
            return
            
        columns = ("id", "first_name", "last_name", "level", "phone")
        tree = ttk.Treeview(self.results_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=120)
            
        tree.pack(fill="both", expand=True)
        
        for student in results:
            tree.insert("", "end", values=(
                student.get("id", ""),
                student.get("first_name", ""),
                student.get("last_name", ""),
                student.get("level", ""),
                student.get("phone", "")
            ))
            
        tree.bind("<Double-1>", lambda e: self.show_student_details(tree.item(tree.selection()[0], "values")[0]))

    def show_student_details(self, student_id, active_tab=0):
        student = self.model.get_student_by_id(student_id)
        if not student:
            return
            
        self.clear_main_frame()
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        header_frame.pack(fill="x", pady=10)
        tk.Label(header_frame, text=f"{student.get('first_name')} {student.get('last_name')}", 
                 font=("Helvetica", 20, "bold"), bg="#ecf0f1").pack(side="left")
        
        tk.Button(header_frame, text="Delete", command=lambda: self.delete_student(student_id), 
                 bg="#e74c3c", fg="white").pack(side="right", padx=10)

        # Tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True, pady=10)

        # Tab 1: Profile
        profile_tab = tk.Frame(notebook, bg="white")
        notebook.add(profile_tab, text="Profile")
        
        details_frame = tk.Frame(profile_tab, bg="white", padx=20, pady=20)
        details_frame.pack(fill="x")
        
        row = 0
        col = 0
        for key, value in student.items():
            if key in ["attendance", "payments"]: continue
            tk.Label(details_frame, text=key.replace("_", " ").title() + ":", 
                     font=("Helvetica", 10, "bold"), bg="white").grid(row=row, column=col, sticky="e", padx=5, pady=5)
            tk.Label(details_frame, text=str(value), bg="white").grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
            
            col += 2
            if col > 2:
                col = 0
                row += 1

        # Quick Actions in Profile
        actions_frame = tk.Frame(profile_tab, bg="white")
        actions_frame.pack(fill="x", pady=20, padx=20)
        
        tk.Button(actions_frame, text="Record Attendance", 
                 command=lambda: self.record_attendance_dialog(student),
                 bg="#9b59b6", fg="white").pack(side="left", padx=10)
                 
        tk.Button(actions_frame, text="Record Payment", 
                 command=lambda: self.record_payment_dialog(student),
                 bg="#f1c40f", fg="black").pack(side="left", padx=10)

        # Tab 2: Attendance
        attendance_tab = tk.Frame(notebook, bg="white")
        notebook.add(attendance_tab, text="Attendance History")
        
        att_columns = ("date", "status", "notes")
        att_tree = ttk.Treeview(attendance_tab, columns=att_columns, show="headings")
        att_tree.heading("date", text="Date")
        att_tree.heading("status", text="Status")
        att_tree.heading("notes", text="Notes")
        att_tree.column("date", width=100)
        att_tree.column("status", width=100)
        att_tree.column("notes", width=300)
        att_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        for record in student.get("attendance", []):
            att_tree.insert("", "end", values=(
                record.get("date", ""),
                record.get("status", ""),
                record.get("notes", "")
            ))
            
        tk.Button(attendance_tab, text="Add New Record", 
                 command=lambda: self.record_attendance_dialog(student),
                 bg="#9b59b6", fg="white").pack(pady=10)

        # Tab 3: Payments
        payment_tab = tk.Frame(notebook, bg="white")
        notebook.add(payment_tab, text="Payment History")
        
        pay_columns = ("date", "amount", "description")
        pay_tree = ttk.Treeview(payment_tab, columns=pay_columns, show="headings")
        pay_tree.heading("date", text="Date")
        pay_tree.heading("amount", text="Amount")
        pay_tree.heading("description", text="Description")
        pay_tree.column("date", width=100)
        pay_tree.column("amount", width=100)
        pay_tree.column("description", width=300)
        pay_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        for record in student.get("payments", []):
            pay_tree.insert("", "end", values=(
                record.get("date", ""),
                f"{record.get('amount', 0):.2f}",
                record.get("description", "")
            ))

        tk.Button(payment_tab, text="Add New Payment", 
                 command=lambda: self.record_payment_dialog(student),
                 bg="#f1c40f", fg="black").pack(pady=10)

        if active_tab:
            try:
                notebook.select(active_tab)
            except:
                pass


    def delete_student(self, student_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            if self.model.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted.")
                self.show_all_students()
            else:
                messagebox.showerror("Error", "Could not delete student.")

    def attendance_tracker(self):
        self.show_all_students(
            title="Attendance: Select Student",
            on_click=lambda student_id: self.show_student_details(student_id, active_tab=1)
        )

    def payment_tracker(self):
        self.show_all_students(
            title="Payments: Select Student",
            on_click=lambda student_id: self.show_student_details(student_id, active_tab=2)
        )

    def record_attendance_dialog(self, student):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Attendance for {student.get('first_name')}")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = ttk.Entry(dialog)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        tk.Label(dialog, text="Status:").pack(pady=5)
        status_combo = ttk.Combobox(dialog, values=["Present", "Absent", "Late"], state="readonly")
        status_combo.current(0)
        status_combo.pack(pady=5)
        
        tk.Label(dialog, text="Notes:").pack(pady=5)
        notes_entry = ttk.Entry(dialog)
        notes_entry.pack(pady=5)
        
        def save():
            self.model.add_attendance(student["id"], date_entry.get(), status_combo.get(), notes_entry.get())
            messagebox.showinfo("Saved", "Attendance recorded.")
            dialog.destroy()
            
        tk.Button(dialog, text="Save", command=save, bg="#27ae60", fg="white").pack(pady=20)

    def record_payment_dialog(self, student):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Payment for {student.get('first_name')}")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog)
        amount_entry.pack(pady=5)
        
        tk.Label(dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = ttk.Entry(dialog)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        tk.Label(dialog, text="Description:").pack(pady=5)
        desc_entry = ttk.Entry(dialog)
        desc_entry.pack(pady=5)
        
        def save():
            try:
                amount = float(amount_entry.get())
                self.model.add_payment(student["id"], amount, date_entry.get(), desc_entry.get())
                messagebox.showinfo("Saved", "Payment recorded.")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
            
        tk.Button(dialog, text="Save", command=save, bg="#27ae60", fg="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
