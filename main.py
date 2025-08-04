from task_manager import create_task, Priority, lm, save_tasks, import_tasks, Operation
from utils import clear_terminal

def main_menu():
    """
    Displays the main menu for the Task Manager application.
    Allows the user to interact with the program by selecting options to create tasks,
    view task lists, save tasks, import tasks, start a Pomodoro timer, or delete tasks.
    """
    while True:
        clear_terminal()
        print("Task Manager")
        print("1. Create a new task")
        print("2. Show task lists")
        print("3. Save tasks")
        print("4. Import tasks")
        print("5. Start Pomodoro")
        print("6. Delete a task")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_new_task()
        elif choice == "2":
            lm.show_lists()
            input("Press Enter to continue...")
        elif choice == "3":
            save_tasks()
            print("Tasks saved successfully!")
            input("Press Enter to continue...")
        elif choice == "4":
            import_tasks()
            print("Tasks imported successfully!")
            input("Press Enter to continue...")
        elif choice == "5":
            start_pomodoro()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")

def create_new_task():
    """
    Prompts the user to create a new task by providing its name, description,
    priority, and estimated time to complete. The task is then added to the Task Manager.

    Raises:
        ValueError: If the user provides invalid input for the task's estimated time.
    """
    clear_terminal()
    print("Create New Task")
    name = input("Task name: ")
    if name.strip() == "":
        print("Invalid name. Please provide a valid name.")
        input("Press Enter to continue...")
        return     
    
    description = input("Task description: ")
    if description.strip() == "":
        print("Invalid description. Please provide a valid description.")
        input("Press Enter to continue...")
        return   
    
    print("Priority:")
    print("1. Low")
    print("2. Medium")
    print("3. High")
    priority_choice = input("Choose the priority (1/2/3): ")

    if priority_choice == "1":
        priority = Priority.LOW
    elif priority_choice == "2":
        priority = Priority.MID
    elif priority_choice == "3":
        priority = Priority.HIGH
    else:
        print("Invalid priority. Task not created.")
        input("Press Enter to continue...")
        return

    try:
        conclude_time = float(input("Estimated time to complete (in minutes): "))
        task = create_task(name, description, priority, conclude_time)
        print("Task created successfully:")
        print(task)
    except ValueError:
        print("Invalid time. Task not created.")

    input("Press Enter to continue...")

def start_pomodoro():
    """
    Prompts the user to start a Pomodoro timer for a specific task.
    The user must provide the task name, break time, and the number of Pomodoro cycles.

    Raises:
        ValueError: If the user provides invalid input for break time or number of cycles.
    """
    clear_terminal()
    print("Start Pomodoro")
    lm.show_lists()
    task_name = input("Enter the name of the task to start the Pomodoro: ")

    for task_list in [lm.task_low, lm.task_mid, lm.task_high]:
        for task in task_list:
            if task.task_name == task_name:
                try:
                    break_time = float(input("Break time (in minutes): "))
                    repeat_times = int(input("Number of Pomodoro cycles: "))
                    task.start_pomodoro(break_time, "Break", repeat_times)
                    return
                except ValueError:
                    print("Invalid input. Operation canceled.")
                    input("Press Enter to continue...")
                    return

    print("Task not found.")
    input("Press Enter to continue...")

def delete_task():
    """
    Prompts the user to delete a specific task by providing its name.
    The task is removed from the Task Manager if found.
    """
    clear_terminal()
    print("Delete Task")
    lm.show_lists()
    task_name = input("Enter the name of the task to delete: ")

    for task_list in [lm.task_low, lm.task_mid, lm.task_high]:
        for task in task_list:
            if task.task_name == task_name:
                lm.list_manager(task, Operation.DELETE)
                print("Task deleted successfully.")
                input("Press Enter to continue...")
                return

    print("Task not found.")
    input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()

