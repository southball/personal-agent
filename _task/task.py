from dataclasses import dataclass
import sys

@dataclass
class TaskData:
    name: str = None
    description: str = None
    depends: list[str] = None
    task: callable = None

tasks: dict[str, TaskData] = {}
def task(*, description: str = None, depends: list[str] = None):
    def decorator(func):
        global tasks
        tasks[func.__name__] = TaskData(
            name=func.__name__,
            description=description,
            depends=depends,
            task=func
        )
    return decorator

def help():
    print("Available tasks:")
    for name, task_data in tasks.items():
        desc = task_data.description if task_data.description else "(No description)"
        print(f"  {name}: {desc}")

def runner():
    if len(sys.argv) < 2:
        help()
        sys.exit(1)
    
    task = sys.argv[1]

    finished_tasks: set[str] = set()
    def run_task(task_name: str):
        if task_name in finished_tasks:
            return
        if task_name not in tasks:
            print(f"Task {task_name} not found.")
            sys.exit(1)
        task_data = tasks[task_name]
        if task_data.depends:
            for dep in task_data.depends:
                run_task(dep)
        print(f"Running task {task_name}...")
        task_data.task()
        finished_tasks.add(task_name)

    run_task(task)
