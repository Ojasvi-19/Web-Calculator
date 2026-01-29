# calculator.py

def add(a, b):
    try:
        return a + b
    except TypeError:
        return "Invalid input"


def sub(a, b):
    try:
        return a - b
    except TypeError:
        return "Invalid input"


def mul(a, b):
    try:
        return a * b
    except TypeError:
        return "Invalid input"


def div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except TypeError:
        raise ValueError("Invalid input")
