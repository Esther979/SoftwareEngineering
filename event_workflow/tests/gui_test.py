import sys
import os
sys.path.append(os.path.abspath("../"))

import unittest
import tkinter as tk
from unittest.mock import patch
from app.event_workflow_gui import SEPApp
from workflow.event_workflow import WorkflowSystem


class TestSEPAppGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 不显示窗口
        self.app = SEPApp(self.root)
        self.system = self.app.system

    def tearDown(self):
        self.root.destroy()

    def test_create_event_application_via_gui(self):
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.create_login_screen()
            self.app.role_var.set("CustomerService")
            self.app.login()
            self.app.create_event()

            # 获取所有 Entry
            fields = self.app.root.winfo_children()
            entries = [w for w in fields if isinstance(w, tk.Entry)]

            # 填写模拟输入
            entries[0].insert(0, "TestCorp")
            entries[1].insert(0, "Workshop")
            entries[2].insert(0, "2025-12-01")
            entries[3].insert(0, "2025-12-02")
            entries[4].insert(0, "5000")
            entries[5].insert(0, "Audio, Decor")

            # 提交按钮
            submit_button = [w for w in fields if isinstance(w, tk.Button) and w['text'] == "Submit"][0]
            submit_button.invoke()

            # 验证创建成功
            self.assertEqual(len(self.system.applications), 1)
            app_created = self.system.applications[0]
            self.assertEqual(app_created.status, "Pending Review")
            mock_info.assert_called()

    def test_review_application_via_gui(self):
        app_created = self.system.create_event_application(
            "TestCorp", "Workshop", "2025-12-01", "2025-12-02", 5000, "Decor, Audio", "CustomerService"
        )

        # 模拟 SCS 登录并审批
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

        self.assertEqual(app_created.status, "Forwarded")
        history_records = [(r[2], r[1], r[3]) for r in app_created.history]
        self.assertIn(("Forwarded", "SCS", ""), history_records)

    # 🧩 新增测试：验证审批顺序（FM 必须在 AM 之前）
    def test_workflow_order_enforcement(self):
        app_created = self.system.create_event_application(
            "ClientA", "Conference", "2025-11-10", "2025-11-12", 8000, "Decor", "CustomerService"
        )

        # ❌ AM 尝试提前审批（FM 还没处理）
        with self.assertRaises(ValueError):
            self.system.review_application(app_created.app_id, "AM", "Approved", "Looks fine")

        # ✅ 正确顺序：SCS → FM → AM
        self.system.review_application(app_created.app_id, "SCS", "Forwarded", "Sent to FM")
        self.system.review_application(app_created.app_id, "FM", "Forwarded", "Budget OK")
        self.system.review_application(app_created.app_id, "AM", "Approved", "All good")

        self.assertEqual(app_created.status, "Approved")
        print("\n✅ Workflow order enforced successfully.")

if __name__ == "__main__":
    unittest.main()
