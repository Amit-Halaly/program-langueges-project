from PARSER.parser import *
import math
import os


class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    # Sets the positional attributes for error reporting
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    # Sets the context (for variable scope, etc.)
    def set_context(self, context=None):
        self.context = context
        return self

    # Placeholder for addition operation; returns an illegal operation error
    def added_to(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for subtraction operation; returns an illegal operation error
    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for multiplication operation; returns an illegal operation error
    def multed_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for division operation; returns an illegal operation error
    def dived_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for modulo operation; returns an illegal operation error
    def moduloed_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for equality comparison; returns an illegal operation error
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for inequality comparison; returns an illegal operation error
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for less-than comparison; returns an illegal operation error
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for greater-than comparison; returns an illegal operation error
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for less-than-or-equal comparison; returns an illegal operation error
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for greater-than-or-equal comparison; returns an illegal operation error
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for logical AND operation; returns an illegal operation error
    def anded_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for logical OR operation; returns an illegal operation error
    def ored_by(self, other):
        return None, self.illegal_operation(other)

    # Placeholder for logical NOT operation; returns an illegal operation error
    def notted(self,other):
        return None, self.illegal_operation(other)

    # Executes a value (if callable); returns an illegal operation error
    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    # Placeholder for copying the value; should be overridden by subclasses
    def copy(self):
        raise Exception('No copy method defined')

    # Determines if the value is "truthy"; should be overridden by subclasses
    def is_true(self):
        return False

    # Generates an error for illegal operations
    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RTError(self.pos_start, other.pos_end, 'Illegal operation', self.context)


class Number(Value):
    def __init__(self, value):
       super().__init__()
       self.value = value

    # Performs addition between two numbers
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs subtraction between two numbers
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs multiplication between two numbers
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs modulus operation between two numbers
    def moduloed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs division between two numbers and checks for division by zero
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero', self.context)

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if two numbers are equal
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if two numbers are not equal
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if one number is less than another
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if one number is greater than another
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if one number is less than or equal to another
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Checks if one number is greater than or equal to another
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs logical AND operation between two numbers
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs logical OR operation between two numbers
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Performs logical NOT operation on a number
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    # Creates a copy of the number
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    # Determines if the number is "truthy" (non-zero)
    def is_true(self):
        return self.value != 0

    # Returns the string representation of the number
    def __repr__(self):
        return str(self.value)


# Predefined constants for common numbers
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    # Concatenates two string.
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Repeats a string by multiplying it with a number
    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    # Determines if the string is "truthy" (non-empty)
    def is_true(self):
        return len(self.value) > 0

    # Creates a copy of the string
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    # Returns the string representation of the string value
    def __str__(self):
        return self.value

    # Returns the string representation of the string for debugging
    def __repr__(self):
        return f'"{self.value}"'


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    # Adds an element to the list
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    # Removes an element from the list by index
    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(other.pos_start, other.pos_end, 'Element at this index could not be removed from list because index is out of bounds', self.context)
        else:
            return None, Value.illegal_operation(self, other)

    # Multiplies the list by replicating its elements a specified number of times
    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    # Divides the list by getting an element at a specific index
    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(other.pos_start, other.pos_end, 'Element at this index could not be retrieved from list because index is out of bounds', self.context)
        else:
            return None, Value.illegal_operation(self, other)

    # Creates a copy of the list
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    # Returns the string representation of the list for debugging
    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    # Generates a new context for function execution
    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    # Generates an error if the correct number of arguments is not provided
    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(args) - len(arg_names)} too many args passed into {self}", self.context))

        if len(args) < len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end, f"{len(arg_names) - len(args)} too few args passed into {self}", self.context))

        return res.success(None)

    # Populates the arguments into the current context's symbol table
    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    # Generates a new context for executing the function
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    # Executes the function with the provided arguments
    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    # Creates a copy of the function
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    # Returns the string representation of the function
    def __repr__(self):
        return f"<function {self.name}>"


class Lambda(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    # Executes the lambda function with the provided arguments
    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    # Creates a copy of the lambda function
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    # Returns the string representation of the lambda function
    def __repr__(self):
        return f"<lambda {self.name}>"


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    # Executes the built-in function with the provided arguments
    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res
        return res.success(return_value)

    # Returns an error if the built-in function does not exist
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    # Returns the string representation of the built-in function
    def __repr__(self):
        return f"<built-in function {self.name}>"

    #####################################
    # Executes the "print" built-in function
    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']

    # Executes the "input" built-in function to get user input
    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(text)
    execute_input.arg_names = []

    # Executes the "input_int" built-in function to get integer input from the user
    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []

    # Executes the "clear" built-in function to clear the console
    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    # Executes the "is_number" built-in function to check if a value is a number
    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]

    # Executes the "is_function" built-in function to check if a value is a function
    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    # Executes the "run" built-in function to run a script file
    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")
        if not isinstance(fn, String):
            return RTResult().failure(RTError(self.pos_start, self.pos_end, "Second argument must be string", exec_ctx))
        if fn.value.endswith('.lambda'):
            fn = fn.value

            try:
                with open(fn, "r") as f:
                    script = f.read()
            except Exception as e:
                return RTResult().failure(RTError(self.pos_start, self.pos_end, f"Failed to load script \"{fn}\"\n" + str(e), exec_ctx))

            _, error = run(fn, script)

            if error:
                return RTResult().failure(RTError(self.pos_start, self.pos_end, f"Failed to finish executing script \"{fn}\"\n" + error.as_string(), exec_ctx))

            return RTResult().success(Number.null)

        return RTResult().failure(RTError(self.pos_start, self.pos_end, "file name needs to end with '.lambda'", exec_ctx))

    execute_run.arg_names = ["fn"]


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.run = BuiltInFunction("run")


class Interpreter:
    # Dispatches node to the appropriate visit method based on its type
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    # Default method for unhandled node types
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################
    # Handles number nodes by returning their value
    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    # Handles list nodes by evaluating each element and returning a list
    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    # Handles variable access by retrieving its value from the symbol table
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    # Handles boolean access by retrieving its value from the symbol table
    def visit_BoolAccessNode(self, node, context):
        res = RTResult()
        bool_name = node.bool_name_tok.value
        value = context.symbol_table.get(bool_name)

        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end, f"'{bool_name}' is not defined", context))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    # Handles binary operations (e.g., +, -, *, /) by evaluating both sides and performing the operation
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return():
            return res
        if node.op_tok.matches(TT_KEYWORD, 'or'):
            if left.value == 1:
                return res.success(left)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            if left.value == 0:
                return res.success(left)
        right = res.register(self.visit(node.right_node, context))
        if res.should_return():
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MODULO:
            result, error = left.moduloed_by(right)
        elif node.op_tok.type == TT_EQ:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    # Handles unary operations (e.g., -x, not x) by applying the operation to a single operand
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res

        error = None
        # Apply the appropriate unary operation based on the operator token
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    # Handles string nodes by returning their value
    def visit_StringNode(self, node, context):
        return RTResult().success(String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    # Handles function definitions by creating a function object and adding it to the symbol table
    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    # Handles lambda definitions similarly to functions, but for anonymous functions.
    def visit_LambdaDefNode(self, node, context):
        res = RTResult()

        lambda_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        lambda_value = Lambda(lambda_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(lambda_name, lambda_value)

        return res.success(lambda_value)

    # Handles function calls by evaluating the function and its arguments, then executing it.
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res
        # Execute the function with the evaluated arguments.
        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    # Handles return statements by returning the value from the function
    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number.null

        return res.success_return(value)


# RUNTIME RESULT #######
class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        # Indicates if the current operation should terminate early (e.g., due to an error or return value)
        # Note: this will allow you to continue and break outside the current function
        return self.error or self.func_return_value


# CONTEXT #########
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


# SYMBOL TABLE
class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


# Initialize global symbol table with built-in functions and constants
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("PI", Number.math_PI)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("isNum", BuiltInFunction.is_number)
global_symbol_table.set("isFunc", BuiltInFunction.is_function)
global_symbol_table.set("run", BuiltInFunction.run)

# Runs the program by generating tokens, parsing them, and interpreting the AST
def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

