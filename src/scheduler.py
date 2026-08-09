import datetime
import time
import threading


scheduled_tasks = []


def schedule(task_time, function):
    scheduled_tasks.append({
        "time": task_time,
        "function": function,
        "completed": False
    })

    print(f"Scheduled {function.__name__} for {task_time}")


def scheduler_loop():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        for task in scheduled_tasks:
            if current_time == task["time"] and not task["completed"]:
                task["function"]()
                task["completed"] = True

        time.sleep(1)


def start_scheduler():
    threading.Thread(
        target=scheduler_loop,
        daemon=True
    ).start()