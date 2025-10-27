import tkinter as tk
from tkinter import messagebox, ttk
from workflow.event_workflow import WorkflowSystem


system = WorkflowSystem()

class SEPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SEP Event Workflow System")
        self.root.geometry("800x500")
        self.current_role = None
        self.system = WorkflowSystem()

        self.create_login_screen()

    # ------------------- Login -------------------
    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 18, "bold")).pack(pady=30)
        roles = ["CustomerService", "SCS", "FM", "AM"]
        self.role_var = tk.StringVar(value=roles[0])
        ttk.Combobox(self.root, textvariable=self.role_var, values=roles, state="readonly").pack(pady=10)
        tk.Button(self.root, text="Login", width=20, command=self.login).pack(pady=10)

    def login(self):
        self.current_role = self.role_var.get()
        self.create_main_menu()

    # ------------------- Main Menu -------------------
    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_role}", font=("Arial", 16, "bold")).pack(pady=20)

        if self.current_role == "CustomerService":
            tk.Button(self.root, text="Create Event Application", width=30, command=self.create_event).pack(pady=10)
        else:
            tk.Button(self.root, text="View All Applications", width=30, command=self.show_applications).pack(pady=10)
            tk.Button(self.root, text="Review Application", width=30, command=self.review_application).pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.create_login_screen).pack(pady=20)

    # ------------------- Create Event -------------------
    def create_event(self):
        self.clear_screen()
        tk.Label(self.root, text="Create New Event Application", font=("Arial", 16, "bold")).pack(pady=10)
        fields = {}
        labels = ["Client Name", "Event Type", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)", "Budget", "Preferences"]
        for label in labels:
            tk.Label(self.root, text=label + ":").pack()
            entry = tk.Entry(self.root, width=50)
            entry.pack(pady=5)
            fields[label] = entry

        def submit():
            client = fields["Client Name"].get().strip()
            event_type = fields["Event Type"].get().strip()
            start_date = fields["Start Date (YYYY-MM-DD)"].get().strip()
            end_date = fields["End Date (YYYY-MM-DD)"].get().strip()
            budget = fields["Budget"].get().strip()
            preferences = fields["Preferences"].get().strip()

            if not all([client, event_type, start_date, end_date, budget, preferences]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                budget = float(budget)
                app = self.system.create_event_application(
                    client_name=client,
                    event_type=event_type,
                    start_date=start_date,
                    end_date=end_date,
                    budget=budget,
                    preferences=preferences,
                    created_by="CustomerService"
                )
                messagebox.showinfo("Success", f"Application created:\n{app}")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid budget value!")

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)

    # ------------------- View All Applications -------------------
    def show_applications(self):
        self.clear_screen()
        tk.Label(self.root, text="All Event Applications", font=("Arial", 16, "bold")).pack(pady=10)

        if self.current_role == "AM":
            columns = ("id", "client", "type", "status", "FM Feedback")
        else:
            columns = ("id", "client", "type", "status")

        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
        tree.pack(fill=tk.BOTH, expand=True)

        for app in self.system.applications:
            if self.current_role == "AM":
                tree.insert("", tk.END, values=(app.app_id, app.client_name, app.event_type, app.status, app.comment))
            else:
                tree.insert("", tk.END, values=(app.app_id, app.client_name, app.event_type, app.status))

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    # ------------------- Review Application -------------------
    def review_application(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Review Application ({self.current_role})", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Enter Application ID:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack(pady=5)

        tk.Label(self.root, text="Decision:").pack()
        decision_var = tk.StringVar()

        if self.current_role == "SCS":
            decisions = ["Forwarded", "Rejected"]
        elif self.current_role == "FM":
            decisions = ["Forwarded"]
        elif self.current_role == "AM":
            decisions = ["Approved", "Rejected"]
        else:
            decisions = []

        ttk.Combobox(self.root, textvariable=decision_var, values=decisions, state="readonly").pack(pady=5)

        # FM_Feedback
        comment_entry = None
        if self.current_role == "FM":
            tk.Label(self.root, text="Comment / Feedback:").pack()
            comment_entry = tk.Entry(self.root, width=50)
            comment_entry.pack(pady=5)

        def submit():
            try:
                app_id = int(id_entry.get())
                app = self.system.get_application_by_id(app_id)

                if self.current_role == "FM" and app.status != "Forwarded":
                    messagebox.showerror("Error", "FM can only act if SCS Forwarded")
                    return
                if self.current_role == "AM" and app.status != "Forwarded":
                    messagebox.showerror("Error", "AM can only act if SCS and FM Forwarded")
                    return
                if app.status == "Rejected":
                    messagebox.showerror("Error", "This application has been rejected. No further action allowed.")
                    return

                comment_text = comment_entry.get() if comment_entry else ""
                # 记录 comment 到 history
                self.system.review_application(app_id, self.current_role, decision_var.get(), comment_text)
                messagebox.showinfo("Success", f"{self.current_role} set application #{app_id} to {decision_var.get()}")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Submit Review", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)


    # ------------------- Clear Screen -------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SEPApp(root)
    root.mainloop()
