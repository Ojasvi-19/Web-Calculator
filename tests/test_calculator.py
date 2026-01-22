import sys
import os

# Add "web calculator" directory to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "web calculator")
    )
)

from Calculator import Calculator   # importing Flask app
from Calculator import add, sub, mul, div


def test_addition():
    client = Calculator.test_client()
    response = client.post(
        "/",
        data={
            "num1": "10",
            "num2": "5",
            "operation": "add"
        }
    )
    assert response.status_code == 200
    assert b"15" in response.data


def test_subtraction():
    client = Calculator.test_client()
    response = client.post(
        "/",
        data={
            "num1": "10",
            "num2": "5",
            "operation": "sub"
        }
    )
    assert response.status_code == 200
    assert b"5" in response.data


def test_multiplication():
    client = Calculator.test_client()
    response = client.post(
        "/",
        data={
            "num1": "4",
            "num2": "5",
            "operation": "mul"
        }
    )
    assert response.status_code == 200
    assert b"20" in response.data


def test_division():
    client = Calculator.test_client()
    response = client.post(
        "/",
        data={
            "num1": "10",
            "num2": "2",
            "operation": "div"
        }
    )
    assert response.status_code == 200
    assert b"5.0" in response.data


def test_division_by_zero():
    client = Calculator.test_client()
    response = client.post(
        "/",
        data={
            "num1": "10",
            "num2": "0",
            "operation": "div"
        }
    )
    assert response.status_code == 200
    assert b"Error: Division by zero" in response.data