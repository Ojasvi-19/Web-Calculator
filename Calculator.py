from flask import Flask, render_template, request
from Calculator_ops import add,sub,mul,div

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
                result = add(num1, num2)
            elif operation == "sub":
                result = sub(num1, num2)
            elif operation == "mul":
                result = mul(num1, num2)
            elif operation == "div":
                result = div(num1, num2)

        except Exception as e:
            result = str(e)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    Calculator.run(debug=True)


