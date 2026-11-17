
import operator

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
}


def calculator():
    print("-- Python Calculator --")
    print("Supported operations: +, -, *, /, ^")

    while True:
        op = input("\nEnter operator (+, -, *, /, ^) or 'q' to quit: ").strip()

        if op.lower() == 'q':
            print("Exiting calculator. Bye!")
            break

        if op not in OPERATIONS:
            print("Invalid choice. Please select a valid operator.")
            continue

        try:
            num1_input = input("Enter the first number: ").strip()

            if num1_input.lower() == 'q':
                break

            num1 = float(num1_input)

            num2_input = input("Enter the second number: ").strip()

            if num2_input.lower() == 'q':
                break

            num2 = float(num2_input)

        except ValueError:
            print("Invalid input. Please enter valid numeric values.")
            continue

        if op == "/" and num2 == 0:
            print("Error: Cannot divide by zero.")
            continue

        result = OPERATIONS[op](num1, num2)

        print(f"Result: {result}")


if __name__ == "__main__":
    calculator()
