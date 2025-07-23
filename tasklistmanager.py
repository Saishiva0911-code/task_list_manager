import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

TASK_FILE = "tasks.txt"

def load_tasks():
    tasks = []
    if not os.path.exists(TASK_FILE):
        return tasks
    with open(TASK_FILE, "r") as f:
        for line in f:
            task, due, done = line.strip().split("|")
            tasks.append({"task": task, "due": due, "done": done == "True"})
    return tasks

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        for t in tasks:
            f.write(f"{t['task']}|{t['due']}|{t['done']}\n")

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Task Manager")
        self.tasks = load_tasks()

        # Entry fields
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=5)
        self.due_entry = tk.Entry(root, width=20)
        self.due_entry.grid(row=0, column=1, padx=10, pady=5)
        self.due_entry.insert(0, "YYYY-MM-DD")

        tk.Button(root, text="Add Task", command=self.add_task).grid(row=0, column=2, padx=10, pady=5)

        # Lists
        tk.Label(root, text="Pending Tasks").grid(row=1, column=0, padx=10)
        self.pending_listbox = tk.Listbox(root, width=60)
        self.pending_listbox.grid(row=2, column=0, columnspan=2, padx=10)

        tk.Button(root, text="Mark as Done ✅", command=self.mark_done).grid(row=2, column=2, padx=10)

        tk.Label(root, text="Completed Tasks").grid(row=3, column=0, padx=10)
        self.completed_listbox = tk.Listbox(root, width=60)
        self.completed_listbox.grid(row=4, column=0, columnspan=2, padx=10)

        self.refresh_lists()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        due_date = self.due_entry.get().strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return
        if not task_text:
            messagebox.showwarning("Missing Task", "Enter a task description.")
            return

        self.tasks.append({"task": task_text, "due": due_date, "done": False})
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.refresh_lists()

    def refresh_lists(self):
        self.pending_listbox.delete(0, tk.END)
        self.completed_listbox.delete(0, tk.END)
        for i, t in enumerate(self.tasks):
            text = f"{t['task']} (Due: {t['due']})"
            if t["done"]:
                self.completed_listbox.insert(tk.END, text)
            else:
                self.pending_listbox.insert(tk.END, f"{i+1}. {text}")

    def mark_done(self):
        selection = self.pending_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Task Selected", "Please select a task to mark as done.")
            return
        index = selection[0]
        count = 0
        for i, t in enumerate(self.tasks):
            if not t["done"]:
                if count == index:
                    self.tasks[i]["done"] = True
                    break
                count += 1
        save_tasks(self.tasks)
        self.refresh_lists()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
