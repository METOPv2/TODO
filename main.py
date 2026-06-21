import customtkinter as ctk
from datetime import datetime
import json
import os
import sys


def _tasks_file() -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "tasks.json")


class TODOApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TODO List")
        self.geometry("820x580")
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.tasks, self.next_id = self._load_tasks()

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="~~~ TODO APP ~~~", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 10))

        # Input row
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.task_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Enter a task...", height=40, font=ctk.CTkFont(size=14)
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda _: self.add_task())

        ctk.CTkButton(input_frame, text="Add Task", width=110, height=40, command=self.add_task).pack(side="right")

        # Sort row
        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(fill="x", padx=20, pady=(0, 4))

        ctk.CTkLabel(sort_frame, text="Sort:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 8))
        for label, key in [("Newest", "newest"), ("Oldest", "oldest"), ("Completed", "completed"), ("On-going", "ongoing")]:
            ctk.CTkButton(
                sort_frame, text=label, width=95, height=30,
                command=lambda k=key: self.sort_tasks(k)
            ).pack(side="left", padx=3)

        # Status bar
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(pady=(2, 4))

        # Task list
        self.task_frame = ctk.CTkScrollableFrame(self, label_text="Tasks")
        self.task_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._refresh()

    # --- Persistence ---

    def _load_tasks(self):
        path = _tasks_file()
        if not os.path.exists(path):
            return [], 1
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            tasks = [
                {**t, "when_created": datetime.fromisoformat(t["when_created"])}
                for t in data
            ]
            next_id = max((t["id"] for t in tasks), default=0) + 1
            return tasks, next_id
        except Exception:
            return [], 1

    def _save_tasks(self):
        path = _tasks_file()
        data = [
            {**t, "when_created": t["when_created"].isoformat()}
            for t in self.tasks
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # --- Actions ---

    def add_task(self):
        content = self.task_entry.get().strip()
        if not content:
            self._status("Cannot add an empty task.", error=True)
            return
        self.tasks.append({
            "id": self.next_id,
            "content": content,
            "completed": False,
            "when_created": datetime.now(),
        })
        self.next_id += 1
        self.task_entry.delete(0, "end")
        self._save_tasks()
        self._status("Task added!")
        self._refresh()

    def sort_tasks(self, key):
        n = len(self.tasks)
        for i in range(n - 1):
            for j in range(i + 1, n):
                a, b = self.tasks[i], self.tasks[j]
                swap = False
                match key:
                    case "newest":
                        swap = a["when_created"] < b["when_created"]
                    case "oldest":
                        swap = a["when_created"] > b["when_created"]
                    case "completed":
                        swap = not a["completed"] and b["completed"]
                    case "ongoing":
                        swap = a["completed"] and not b["completed"]
                if swap:
                    self.tasks[i], self.tasks[j] = b, a
        self._save_tasks()
        self._status(f"Sorted by {key}.")
        self._refresh()

    def mark_completed(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = True
                break
        self._save_tasks()
        self._status(f"Task #{task_id} marked as completed.")
        self._refresh()

    def mark_ongoing(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = False
                break
        self._save_tasks()
        self._status(f"Task #{task_id} marked as on-going.")
        self._refresh()

    def remove_task(self, task_id):
        for i, t in enumerate(self.tasks):
            if t["id"] == task_id:
                del self.tasks[i]
                self._save_tasks()
                self._status(f"Task #{task_id} deleted.")
                self._refresh()
                return

    # --- UI helpers ---

    def _status(self, msg, error=False):
        self.status_label.configure(text=msg, text_color="red" if error else "gray")

    def _refresh(self):
        for w in self.task_frame.winfo_children():
            w.destroy()

        if not self.tasks:
            ctk.CTkLabel(
                self.task_frame, text="No tasks :)", font=ctk.CTkFont(size=14), text_color="gray"
            ).pack(pady=20)
            return

        for task in self.tasks:
            self._render_row(task)

    def _render_row(self, task):
        row = ctk.CTkFrame(self.task_frame)
        row.pack(fill="x", pady=3, padx=2)

        ctk.CTkLabel(row, text="✅" if task["completed"] else "❌", font=ctk.CTkFont(size=15), width=32).pack(
            side="left", padx=(10, 4)
        )
        ctk.CTkLabel(row, text=f"#{task['id']}", font=ctk.CTkFont(size=12), text_color="gray", width=36).pack(
            side="left", padx=(0, 6)
        )
        ctk.CTkLabel(
            row,
            text=task["content"],
            font=ctk.CTkFont(size=14),
            anchor="w",
            text_color="gray" if task["completed"] else "white",
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            row,
            text=task["when_created"].strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(size=11),
            text_color="gray",
        ).pack(side="left", padx=(0, 8))

        tid = task["id"]
        ctk.CTkButton(
            row, text="✅", width=36, height=28, fg_color="#1a6e1a", hover_color="#145214",
            command=lambda t=tid: self.mark_completed(t)
        ).pack(side="left", padx=2)
        ctk.CTkButton(
            row, text="↩", width=36, height=28, fg_color="#555", hover_color="#333",
            command=lambda t=tid: self.mark_ongoing(t)
        ).pack(side="left", padx=2)
        ctk.CTkButton(
            row, text="🗑", width=36, height=28, fg_color="#7a0000", hover_color="#550000",
            command=lambda t=tid: self.remove_task(t)
        ).pack(side="left", padx=(2, 10))


if __name__ == "__main__":
    app = TODOApp()
    app.mainloop()
