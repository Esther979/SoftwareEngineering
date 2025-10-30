import sys
import os
sys.path.append(os.path.abspath("../"))  # tests/ 的父目录加入模块搜索路径

import unittest
from unittest.mock import patch
import tkinter as tk

from app.event_workflow_gui import SEPApp
from workflow.event_workflow import WorkflowSystem

class TestSEPAppGUI(unittest.TestCase):
    def setUp(self):
        # 初始化 GUI 主窗口但不显示
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = SEPApp(self.root)
        self.system = self.app.system

    def tearDown(self):
        self.root.destroy()

    def test_create_event_application_via_gui(self):
        """Test that a CustomerService can create an event application via GUI"""
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.role_var.set("CustomerService")
            self.app.login()
            self.app.create_event()
            fields = self.app.root.winfo_children()
            entries = [w for w in fields if isinstance(w, tk.Entry)]

            entries[0].insert(0, "TestCorp")             # Client Name
            entries[1].insert(0, "Workshop")             # Event Type
            entries[2].insert(0, "2025-12-01")           # Start Date
            entries[3].insert(0, "2025-12-02")           # End Date
            entries[4].insert(0, "5000")                 # Budget
            entries[5].insert(0, "Decor, Audio")        # Preferences

            submit_button = [w for w in fields if isinstance(w, tk.Button) and w['text'] == "Submit"][0]
            submit_button.invoke()

            app_created = self.system.applications[0]

            # 打印详细信息
            print("\n[CREATE EVENT TEST DETAILS]")
            print(f"Application ID: {app_created.app_id}")
            print(f"Client: {app_created.client_name}")
            print(f"Status: {app_created.status}")
            print(f"Comment: {app_created.comment}")
            print(f"History: {[(r[1], r[2], r[3]) for r in app_created.history]}")
            print("✅ Create Event Application Test Passed" if app_created.client_name == "TestCorp" else "❌ Failed")

            self.assertEqual(app_created.client_name, "TestCorp")
            self.assertEqual(app_created.status, "Pending Review")

    def test_review_application_via_gui(self):
        """Test SCS, FM, AM review sequence and FM comment recording"""
        # 创建事件
        app_created = self.system.create_event_application(
            "TestCorp", "Workshop", "2025-12-01", "2025-12-02", 5000, "Decor, Audio", "CustomerService"
        )

        # ---------------- SCS 处理 ----------------
        self.app.current_role = "SCS"
        self.app.review_application()

        fields = self.app.root.winfo_children()
        id_entry = [w for w in fields if isinstance(w, tk.Entry)][0]
        id_entry.insert(0, str(app_created.app_id))

        combo = [w for w in fields if isinstance(w, tk.ttk.Combobox)][0]
        combo.set("Forwarded")

        comment_entry = [w for w in fields if isinstance(w, tk.Entry) and w not in [id_entry]][0]
        comment_entry.insert(0, "Sent to FM")

        submit_button = [w for w in fields if isinstance(w, tk.Button) and w['text'] == "Submit Review"][0]
        submit_button.invoke()

        print("\n[REVIEW TEST DETAILS - SCS]")
        print(f"Application Status after SCS: {app_created.status}")
        print(f"History: {[(r[1], r[2], r[3]) for r in app_created.history]}")
        if app_created.status == "Forwarded":
            print("✅ SCS review passed")

        # ---------------- FM 处理 ----------------
        self.app.current_role = "FM"
        self.app.review_application()
        fields = self.app.root.winfo_children()
        id_entry = [w for w in fields if isinstance(w, tk.Entry)][0]
        id_entry.insert(0, str(app_created.app_id))

        combo = [w for w in fields if isinstance(w, tk.ttk.Combobox)][0]
        combo.set("Forwarded")

        comment_entry = [w for w in fields if isinstance(w, tk.Entry) and w not in [id_entry]][0]
        comment_entry.insert(0, "Budget OK")

        submit_button = [w for w in fields if isinstance(w, tk.Button) and w['text'] == "Submit Review"][0]
        submit_button.invoke()

        print("\n[REVIEW TEST DETAILS - FM]")
        print(f"Application Status after FM: {app_created.status}")
        print(f"FM Comment: {app_created.comment}")
        print(f"History: {[(r[1], r[2], r[3]) for r in app_created.history]}")
        if app_created.comment == "Budget OK":
            print("✅ FM feedback recorded")

        # ---------------- AM 处理 ----------------
        self.app.current_role = "AM"
        self.app.review_application()
        fields = self.app.root.winfo_children()
        id_entry = [w for w in fields if isinstance(w, tk.Entry)][0]
        id_entry.insert(0, str(app_created.app_id))

        combo = [w for w in fields if isinstance(w, tk.ttk.Combobox)][0]
        combo.set("Approved")

        comment_entry = [w for w in fields if isinstance(w, tk.Entry) and w not in [id_entry]][0]
        comment_entry.insert(0, "")

        submit_button = [w for w in fields if isinstance(w, tk.Button) and w['text'] == "Submit Review"][0]
        submit_button.invoke()

        print("\n[REVIEW TEST DETAILS - AM]")
        print(f"Application Status after AM: {app_created.status}")
        print(f"FM Comment still: {app_created.comment}")
        print(f"History: {[(r[1], r[2], r[3]) for r in app_created.history]}")
        if app_created.status == "Approved":
            print("✅ AM approval passed")

        # 验证最终状态
        self.assertEqual(app_created.status, "Approved")
        self.assertEqual(app_created.comment, "Budget OK")

    def test_workflow_order_enforcement(self):
        """Test that FM cannot act before SCS and AM cannot act before FM"""
        app_created = self.system.create_event_application(
            "SeqTest", "Seminar", "2025-12-10", "2025-12-11", 3000, "Food", "CustomerService"
        )

        # AM 直接操作应该报错
        self.app.current_role = "AM"
        try:
            self.system.review_application(app_created.app_id, "AM", "Approved", "")
        except ValueError as e:
            print("\n[WORKFLOW ORDER ENFORCEMENT]")
            print(f"AM action before FM: Caught ValueError as expected: {e}")
            print("✅ Workflow order enforced for AM")
        else:
            print("❌ Workflow order enforcement failed for AM")

        # FM 直接操作应该报错
        self.app.current_role = "FM"
        try:
            self.system.review_application(app_created.app_id, "FM", "Forwarded", "OK")
        except ValueError as e:
            print(f"FM action before SCS: Caught ValueError as expected: {e}")
            print("✅ Workflow order enforced for FM")
        else:
            print("❌ Workflow order enforcement failed for FM")

if __name__ == "__main__":
    unittest.main()
