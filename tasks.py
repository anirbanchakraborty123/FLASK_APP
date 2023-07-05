from celery import Celery

app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@localhost:5672//')

@app.task
def add(x, y):
    return x + y

@app.task
def subtract(x, y):
    return x - y

@app.task
def multiply(x, y):
    return x * y

@app.task
def divide(x, y):
    if y != 0:
        return x / y
    else:
        raise ZeroDivisionError('Cannot divide by zero')

# FUNCTION TO  PROCESS THE TASKS ACCORDING THE PRIORITY
def process_tasks():
    tasks = [
        {'function': add, 'args': [2, 3], 'priority': 1},
        {'function': multiply, 'args': [4, 5], 'priority': 2},
        {'function': subtract, 'args': [6, 7], 'priority': 10},
        {'function': divide, 'args': [10, 5], 'priority': 5}
    ]

    # Sort tasks based on priority (in ascending order)
    tasks.sort(key=lambda x: x['priority'])

    # Execute tasks in order
    for task in tasks:

        result = task['function'].delay(*task['args']).get()
        print(f"Task {task['priority']} Output: {result}")

# Main function
if __name__ == '__main__':
    process_tasks()