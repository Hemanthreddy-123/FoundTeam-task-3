import json
import datetime
import os

class Task:
    def __init__(self, title, description, due_date, priority, tags=None, recurring_interval=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.recurring_interval = recurring_interval

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Task(**data)

    def __str__(self):
        tags_str = ', '.join(self.tags)
        return f"{self.title} - {self.description} - Due: {self.due_date} - Priority: {self.priority} - Tags: {tags_str} - Recurs: {self.recurring_interval if self.recurring_interval else 'No'}"

task_list = []
DATA_FILE = 'tasks.json'
BACKUP_FILE = 'tasks_backup.json'

# Load existing tasks
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return [Task.from_dict(task) for task in data]
    return []

# Save current tasks
def save_tasks():
    with open(DATA_FILE, 'w') as f:
        json.dump([task.to_dict() for task in task_list], f, indent=4)

# Backup tasks
def backup_tasks():
    with open(BACKUP_FILE, 'w') as f:
        json.dump([task.to_dict() for task in task_list], f, indent=4)
    print("Backup saved successfully.\n")

# Restore tasks
def restore_tasks():
    global task_list
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r') as f:
            data = json.load(f)
            task_list = [Task.from_dict(task) for task in data]
            save_tasks()
            print("Backup restored successfully.\n")
    else:
        print("No backup file found.\n")

# Export tasks to file
def export_tasks(filename='tasks_export.txt'):
    with open(filename, 'w') as f:
        for task in task_list:
            f.write(str(task) + '\n')
    print(f"Tasks exported to {filename}\n")

# Core logic
def add_task(title, description, due_date, priority, tags=None, recurring_interval=None):
    task = Task(title, description, due_date, priority, tags, recurring_interval)
    task_list.append(task)
    save_tasks()

def view_tasks():
    if not task_list:
        print("No tasks available.\n")
    for i, task in enumerate(task_list, start=1):
        print(f"{i}. {task}")
    print()

def menu():
    global task_list
    task_list = load_tasks()

    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Backup Tasks")
        print("4. Restore Tasks")
        print("5. Export Tasks")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Title: ")
            description = input("Description: ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            priority = input("Priority (High/Medium/Low): ")
            tags = input("Tags (comma-separated): ").split(",") if input("Add tags? (y/n): ").lower() == 'y' else []
            recurring = input("Recurring (daily/weekly/monthly) or leave blank: ")
            add_task(title, description, due_date, priority, tags, recurring)

        elif choice == '2':
            view_tasks()

        elif choice == '3':
            backup_tasks()

        elif choice == '4':
            restore_tasks()

        elif choice == '5':
            export_tasks()

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    menu()
