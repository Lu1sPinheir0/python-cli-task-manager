import os
import time

def clear_terminal():
    """
    Clears the terminal screen.
    Uses 'cls' for Windows and 'clear' for Unix/Linux/macOS systems.
    """
    os.system("cls" if os.name == "nt" else "clear")

def timer_logic(message: str, time_value: float):
    """
    Implements a countdown timer that updates on the terminal.

    Args:
        message (str): The message to display above the timer.
        time_value (float): The duration of the timer in minutes.
    """
    # Convert minutes to seconds for time.sleep
    total_seconds = time_value * 60
    if total_seconds <= 0:
        print("Timer duration must be positive.")
        return

    end_time = time.time() + total_seconds

    while time.time() < end_time:
        remaining_seconds = end_time - time.time()
        clear_terminal() # Clear before each update
        # Display remaining time in minutes, formatted to two decimal places
        print(f"{message}\nRemaining: {remaining_seconds / 60:.2f} minutes")
        time.sleep(1) # Wait for 1 second

    clear_terminal() # Clear after timer finishes
    print(f"{message}\nTime's up!")