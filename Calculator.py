from flask import Flask, render_template, request

Calculator = Flask(__name__)

@Calculator.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            num1 = float(request.form.get("num1"))
            num2 = float(request.form.get("num2"))
            operation = request.form.get("operation")

            if operation == "add":
                result = num1 + num2
            elif operation == "sub":
                result = num1 - num2
            elif operation == "mul":
                result = num1 * num2
            elif operation == "div":
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2

        except:
            result = "Invalid input"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    Calculator.run(debug=True)


