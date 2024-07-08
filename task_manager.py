import logging
import sys
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_manager.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Task list to store our tasks
tasks = []

def add_task(description):
    try:
        if not description:
            raise ValueError("Task description cannot be empty")
        task = {"id": len(tasks) + 1, "description": description, "completed": False}
        tasks.append(task)
        logging.info(f"Task added: {description}")
    except ValueError as e:
        logging.error(f"Error adding task: {str(e)}")

def list_tasks():
    if not tasks:
        logging.warning("No tasks found")
    else:
        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            print(f"Task {task['id']}: {task['description']} - {status}")
        logging.info("Tasks listed successfully")

def complete_task(task_id):
    try:
        task_id = int(task_id)
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        if task["completed"]:
            raise ValueError(f"Task {task_id} is already completed")
        task["completed"] = True
        logging.info(f"Task {task_id} marked as completed")
    except ValueError as e:
        logging.error(f"Error completing task: {str(e)}")

def main():
    while True:
        print("\n1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            description = input("Enter task description: ")
            add_task(description)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = input("Enter task ID to complete: ")
            complete_task(task_id)
        elif choice == '4':
            logging.info("Application exiting")
            break
        else:
            logging.warning(f"Invalid choice: {choice}")

if __name__ == "__main__":
    logging.info("Application started")
    main()