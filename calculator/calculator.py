import ast
import operator

operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

def calculate(expression):
    try:
        node = ast.parse(expression, mode='eval').body
    except (SyntaxError, TypeError):
        return "Invalid Expression"

    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            op = operations[type(node.op)]
            left = eval_node(node.left)
            right = eval_node(node.right)
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            op = operations[type(node.op)]
            operand = eval_node(node.operand)
            return op(operand)
        else:
            return "Invalid Expression"

    return eval_node(node)

if __name__ == "__main__":
    expression = input("Enter an expression: ")
    result = calculate(expression)
    print(f"Result: {result}")