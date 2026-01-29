# calculator.py

def add(a, b):
    try:
        return a + b
    except TypeError:
        return "Invalid input"


def subtract(a, b):
    try:
        return a - b
    except TypeError:
        return "Invalid input"


def multiply(a, b):
    try:
        return a * b
    except TypeError:
        return "Invalid input"


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Invalid input"
