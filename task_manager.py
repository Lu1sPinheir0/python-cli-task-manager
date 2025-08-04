import utils
from enum import Enum
import json # Imported for data serialization/deserialization (saving/loading tasks).


class Operation(Enum):
    """
    Defines the types of operations that can be performed on task lists.
    Using Enums ensures clarity and prevents string typos,
    as well as limiting valid operation options.
    """
    DELETE = 1  # Represents a deletion operation.
    ADD = 2     # Represents an addition operation.


class Priority(Enum):
    """
    Defines the priority levels for tasks.
    The use of Enums makes the code more readable and robust,
    avoiding 'magic strings' for priorities.
    """
    LOW = 1     # Low priority task.
    MID = 2     # Medium priority task.
    HIGH = 3    # High priority task.


class Task:
    """
    Represents a single task with its attributes: name, description, priority,
    estimated conclusion time, and completion status.
    This class exclusively focuses on 'being' a task, adhering to the Single
    Responsibility Principle (SRP), without concerns about how it's managed or stored.
    """
    def __init__(self, task_name: str, description: str, priority: Priority, conclude_time: float):
        """
        Initializes a new Task instance.

        Includes rigorous validations to ensure task data integrity at creation time.

        Args:
            task_name (str): The name of the task. Must not be empty and must be a string.
            description (str): A detailed description of the task.
            priority (Priority): The priority level of the task (LOW, MID, HIGH).
                                 Must be a member of the Priority Enum.
            conclude_time (float): The estimated time needed to conclude the task, in minutes.
                                   Must be a positive number.

        Raises:
            ValueError: If 'task_name' is invalid, 'priority' is not a valid
                        Priority Enum member, or 'conclude_time' is not a positive number.
        """
        # Input validation for each task attribute.
        # This ensures that the Task is always created in a valid state.
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(priority, Priority):
            raise ValueError("Priority must be a valid Priority Enum member.")
        if not isinstance(conclude_time, (int, float)) or conclude_time <= 0:
            raise ValueError("Duration must be a positive number.")

        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.conclude_time = conclude_time
        self._is_completed = False  # Internal flag to track if the task is completed.
                                    # The underscore indicates it's an internal-use attribute.

    def __repr__(self) -> str:
        """
        Provides a comprehensive string representation of the Task object.
        Ideal for debugging and for a complete view of the instance.
        """
        return (
            f"Name: {self.task_name}\n"
            f"Description: {self.description}\n"
            f"Priority: {self.priority.name}\n"
            f"Time to conclude: {self.conclude_time} minutes\n"
            f"Completed: {self._is_completed}"
        )

    def __str__(self) -> str:
        """
        Provides a concise, user-friendly string representation of the Task object.
        Used for direct printing or quick display in interfaces.
        """
        return f"Name: {self.task_name} - Completed: {self._is_completed}"

    def conclude_task(self):
        """
        Marks the task as completed.
        Prevents the task from being marked as completed multiple times,
        ensuring the operation's idempotence.
        """
        if not self._is_completed:
            self._is_completed = True
            print(f"Task '{self.task_name}' was completed successfully.")
        else:
            print(f"Task '{self.task_name}' is already completed.")

    def start_pomodoro(self, break_time_minutes: float, prompt_message: str, repeat_times: int):
        """
        Starts a Pomodoro timer cycle for the task.

        This method guides the user through work and break intervals,
        following the Pomodoro technique. At the end, it prompts whether
        the task should be marked as completed.

        Args:
            break_time_minutes (float): The duration of the break interval in minutes.
            prompt_message (str): A message to display during the break interval.
            repeat_times (int): The number of Pomodoro work/break cycles to repeat.
        """
        # The total task time is distributed across cycles, so each "work_interval"
        # is the entire task duration.
        work_interval_minutes = self.conclude_time 

        for i in range(repeat_times):
            print(f"\n--- Pomodoro Cycle {i + 1}/{repeat_times} ---")
            
            # Work interval: The timer is started for the work duration.
            utils.timer_logic(f"Work interval for '{self.task_name}'", time_value=work_interval_minutes)
            
            # Break interval: The break is only taken if it's not the last cycle.
            # This follows the common Pomodoro practice of not having an immediate final break.
            if i < repeat_times - 1:
                utils.timer_logic(prompt_message, time_value=break_time_minutes)
            
        print("\nPomodoro cycles finished.")
        
        # Prompts the user to mark the task as completed.
        # A robust loop ensures that the input is validated.
        while True:
            answer = input("Change status to 'Completed'? (enter 1 for Yes, 0 for No): ").strip()
            try:
                if int(answer) == 1:
                    self.conclude_task() # Calls the task's own method to mark it as completed.
                elif int(answer) == 0:
                    print(f"Task '{self.task_name}' status remains unchanged.")
                break # Exits the loop after valid input.
            except ValueError:
                print("Invalid input. Please enter 1 or 0.") # Specific error message for invalid input.

    def _to_dict(self) -> dict:
        """
        Converts the Task object's attributes into a dictionary.
        This format is ideal for serialization (e.g., saving to JSON).
        The underscore in the name indicates it's an internal-use method for the class
        or the TaskManager, not meant to be called directly by the user.
        """
        return {
            "task_name": self.task_name,
            "description": self.description,
            "priority": self.priority.name,  # Stores Enum name as a string for easy serialization.
            "conclude_time": self.conclude_time,
            "_is_completed": self._is_completed # Maintains consistency in attribute naming.
        }

    @classmethod
    def _from_dict(cls, data: dict):
        """
        Creates a Task object from a dictionary.
        This is a class method (@classmethod) used for deserialization
        (e.g., when loading from JSON). It allows constructing a Task from
        flat data without needing a Task instance first.

        Args:
            data (dict): A dictionary containing task data. Expected keys:
                         'task_name', 'description', 'priority', 'conclude_time',
                         and '_is_completed'.

        Returns:
            Task: A new Task instance populated with the provided data.
        """
        # Instantiates the Task using data from the dictionary, converting the priority
        # from a string back to a Priority Enum member.
        task = cls(
            data["task_name"],
            data["description"],
            Priority[data["priority"].upper()], # Converts the string back to the Enum member.
            data["conclude_time"]
        )
        task._is_completed = data["_is_completed"] # Sets the completion status, which is not part of __init__.
        return task


class TaskManager:
    """
    Manages all task-related operations, including adding, removing,
    displaying, saving, and loading tasks.
    This class encapsulates the state (the task lists) and the associated business logic,
    adhering to the principles of Encapsulation and Cohesion.
    This avoids the use of global variables and makes the system modular and testable.
    """
    def __init__(self):
        """
        Initializes the TaskManager with empty lists for each priority level.
        These lists are instance attributes, ensuring that each TaskManager object
        has its own independent set of tasks.
        """
        self.task_low = []
        self.task_mid = []
        self.task_high = []

    def list_manager(self, task: Task, operation: Operation):
        """
        Manages the addition or removal of a task from its respective task list
        based on its priority.

        Args:
            task (Task): The Task object to be managed.
            operation (Operation): The operation to perform (ADD or DELETE).
        """
        # Dynamically selects the target list based on the task's priority name.
        # Uses .name.lower() to match the dictionary keys.
        target_list = {
            "low": self.task_low,
            "mid": self.task_mid,
            "high": self.task_high
        }[task.priority.name.lower()]

        if operation == Operation.DELETE:
            if task in target_list:
                target_list.remove(task)
                print(f"Task '{task.task_name}' removed from {task.priority.name} priority list.")
            else:
                print(f"Task '{task.task_name}' not found in {task.priority.name} priority list.")
        else: # The default operation is ADD if not DELETE.
            target_list.append(task)
            # The addition print message is typically handled by the higher-level function (create_task)
            # or by a logging mechanism.

    def show_lists(self):
        """
        Prints the contents of all task lists (low, mid, high priority)
        maintained by this TaskManager instance.
        """
        print("\n--- Current Task Lists ---")
        print("Low priority tasks:", self.task_low, "\n")
        print("Mid priority tasks:", self.task_mid, "\n")
        print("High priority tasks:", self.task_high, "\n")
        print("--------------------------\n")

# --- Convenience Functions (can be TaskManager methods or auxiliary functions) ---

def create_task(name: str, description: str, priority: Priority, conclude_time: float) -> Task:
    """
    Creates and returns a new Task object.
    This function acts as a 'factory' to create tasks and then
    automatically adds them to the global TaskManager instance (lm).

    Args:
        name (str): The name of the new task.
        description (str): Description of the new task.
        priority (Priority): Priority of the new task.
        conclude_time (float): Estimated time to conclude the task in minutes.

    Returns:
        Task: The newly created Task instance.
    """
    task = Task(name, description, priority, conclude_time)
    lm.list_manager(task, Operation.ADD) # Adds the task to the global TaskManager instance.
    return task

def create_manager():
    """
    Helper function to create and return a single TaskManager instance.
    This can be expanded to load an existing manager or configure it.
    """
    # The TaskManager instance is created and will be used globally within this module.
    # In a larger application, this instance would be passed between functions or
    # managed in a dependency injection system.
    lm = TaskManager()
    return lm

# Creates a global TaskManager instance that will be used by other functions in the module.
# This is the point where the state manager is initialized.
lm = create_manager()

def save_tasks():
    """
    Saves all tasks managed by the global 'lm' TaskManager instance
    to a JSON file named "Task_lists.json".
    Tasks are converted to dictionary format for serialization.
    """
    data = {
        "high": [t._to_dict() for t in lm.task_high], # Accesses the lists from the 'lm' instance.
        "mid": [t._to_dict() for t in lm.task_mid],
        "low": [t._to_dict() for t in lm.task_low],
    }
    try:
        with open("Task_lists.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Tasks successfully exported to 'Task_lists.json'.")
    except IOError as e:
        # Specific error handling for I/O issues (e.g., write permissions).
        print(f"Error saving tasks to file: {e}")


def import_tasks():
    """
    Loads tasks from "Task_lists.json" into the lists of the global 'lm' TaskManager.
    Important: This function does NOT clear the existing TaskManager lists before importing.
    If called multiple times without clearing 'lm' first, it might lead to duplicate tasks.
    In a real application, you might want to add logic to clear the lists or
    check for duplicates before adding.
    """
    try:
        with open("Task_lists.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Iterates through priorities and loads tasks.
            # '.get()' is used for safe dictionary key access, returning an empty list
            # if the key (e.g., "high") is missing in the JSON, preventing errors.
            for task_data in data.get("high", []):
                # Creates a new Task object from the dictionary data.
                # Task._from_dict does not automatically add the task to the TaskManager,
                # so the task needs to be explicitly added.
                task = Task._from_dict(task_data)
                lm.list_manager(task, Operation.ADD) # Adds the loaded task to the TaskManager.
            for task_data in data.get("mid", []):
                task = Task._from_dict(task_data)
                lm.list_manager(task, Operation.ADD)
            for task_data in data.get("low", []):
                task = Task._from_dict(task_data)
                lm.list_manager(task, Operation.ADD)
        print("Tasks successfully imported from 'Task_lists.json'.")
    except FileNotFoundError:
        print("Task_lists.json not found. No tasks to import.")
    except json.JSONDecodeError:
        # Specific handling for malformed JSON.
        print("Error decoding Task_lists.json. File might be corrupted.")
    except Exception as e:
        # Catches other unexpected exceptions to prevent program crashes.
        print(f"An unexpected error occurred during task import: {e}")

