from ERRORS.errors import *
from LAXER.lexer import *


# Node to represent a number in the abstract syntax tree (AST).
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


# Node to represent a string in the AST.
class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


# Node to represent a variable access in the AST.
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


# Node to represent a list in the AST.
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end


# Node to represent a boolean value in the AST.
class BoolAccessNode:
    def __init__(self, bool_name_tok):
        self.bool_name_tok = bool_name_tok
        self.pos_start = self.bool_name_tok.pos_start
        self.pos_end = self.bool_name_tok.pos_end


# Node to represent a binary operation (e.g., addition, subtraction) in the AST.
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    # String representation of the binary operation node.
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


# Node to represent a unary operation (e.g., negation) in the AST.
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok  # The operator token.
        self.node = node    # The operand node.
        self.pos_start = self.op_tok.pos_start  # Starting position of the unary operation.
        self.pos_end = node.pos_end     # Ending position of the unary operation.

    # String representation of the unary operation node.
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


# Node to represent a return statement in the AST.
class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return      # The node representing the value to return.
        self.pos_start = pos_start   # Starting position of the return statement.
        self.pos_end = pos_end   # Ending position of the return statement.


# Node to represent a function definition in the AST.
class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok    # The token representing the function name.
        self.arg_name_toks = arg_name_toks  # List of tokens representing the argument names.
        self.body_node = body_node  # The body of the function.
        self.should_auto_return = should_auto_return    # Whether the function should automatically return the result of its last statement.
        # Determine the start position of the function definition.
        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


# Node to represent a lambda function definition in the AST.
class LambdaDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok  # The token representing the lambda function name (optional).
        self.arg_name_toks = arg_name_toks  # List of tokens representing the argument names.
        self.body_node = body_node  # The body of the lambda function.
        self.should_auto_return = should_auto_return    # Whether the lambda function should automatically return the result of its body.
        # Determine the start position of the lambda function definition.
        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end    # Ending position of the lambda function definition.


# Node to represent a function call in the AST.
class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call     # The node representing the function to be called.
        self.arg_nodes = arg_nodes  # List of nodes representing the arguments passed to the function.
        self.pos_start = self.node_to_call.pos_start    # Starting position of the function call.
        # Determine the ending position of the function call.
        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end


# PARSE RESULT
# Class to manage the result of parsing operations.
class ParseResult:
    def __init__(self):
        self.error = None   # Any error encountered during parsing.
        self.node = None    # The node resulting from the parsing operation.
        self.advance_count = 0   # Number of tokens advanced during parsing.
        self.last_registered_advance_count = 0  # The number of tokens advanced in the last operation.
        self.to_reverse_count = 0     # Number of tokens to reverse if an error occurs.

    # Register the advancement of a token during parsing.
    def register_advancement(self):
        self.advance_count += 1
        self.last_registered_advance_count = 1

    # Register the result of another parsing operation.
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    # Try to register the result of another parsing operation.
    # If an error occurs, set the number of tokens to reverse.
    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    # Mark the parsing operation as successful with a node.
    def success(self, node):
        self.node = node
        return self

    # Mark the parsing operation as a failure with an error.
    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


# PARSER ########
# Main class to handle parsing of tokens into an abstract syntax tree (AST).
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens     # List of tokens to be parsed.
        self.tok_idx = -1   # Current index of the token being processed.
        self.advance()   # Advance to the first token.

    # Advance to the next token.
    def advance(self, ):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    # Reverse by a specified amount of tokens.
    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    # Update the current token based on the current index.
    def update_current_tok(self):
        if self.tok_idx >= 0 & self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    # Main parsing function to parse the tokens into statements.
    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/', '%', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"))
        return res

################################
    # Parses a sequence of statements, handling newlines and multiple statements.
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()
        # Skip newline tokens at the start
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        # Parse the first statement
        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            # Skip newline tokens between statements
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            # Parse additional statements
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))

    # Parses a single statement, including return statements and expressions.
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        # Handle 'return' statements
        if self.current_tok.matches(TT_KEYWORD, 'return'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))
        # Parse a general expression statement
        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'return', 'func', int, identifier, '+', '-', '(', '[' or 'not'"))
        return res.success(expr)

    # Parses a function definition, handling function names, arguments, and bodies.
    def func_def(self):
        res = ParseResult()
        # Check if the function definition starts with 'func'
        if not self.current_tok.matches(TT_KEYWORD, 'func'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected 'func'"))

        res.register_advancement()
        self.advance()
        # Parse function name
        if self.current_tok.type == TT_STR:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected '('"))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier or '('"))

        res.register_advancement()
        self.advance()
        arg_name_toks = []
        # Parse function arguments
        if self.current_tok.type == TT_STR:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_STR:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier"))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ',' or ')'"))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier or ')'"))

        res.register_advancement()
        self.advance()
        # Check for function body
        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(var_name_tok, arg_name_toks, body, True))

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected '->' or NEWLINE"))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected 'end'"))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body, False))

    # Parses a lambda function definition, handling lambda expressions and their arguments.
    def lambda_def(self):
        res = ParseResult()
        # Check if the lambda definition starts with 'lambda'
        if not self.current_tok.matches(TT_KEYWORD, 'lambda'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected lambda"))

        res.register_advancement()
        self.advance()
        # Parse lambda name
        if self.current_tok.type == TT_STR:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected '('"))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier or '('"))

        res.register_advancement()
        self.advance()
        arg_name_toks = []
        # Parse lambda arguments
        if self.current_tok.type == TT_STR:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_STR:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier"))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ',' or ')'"))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected identifier or ')'"))

        res.register_advancement()
        self.advance()
        # Check for lambda body
        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ':'"))

        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        if res.error:
            return res

        return res.success(LambdaDefNode(var_name_tok, arg_name_toks, node_to_return, True))

    # Parses basic elements or "atoms" like integers, strings, variable names, booleans, or parenthesized expressions.
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        # Parse literals and variable access
        if tok.type == TT_INT:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_STR:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_BOOL:
            res.register_advancement()
            self.advance()
            return res.success(BoolAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        # Parse function or lambda definitions
        elif tok.matches(TT_KEYWORD, 'func'):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)
        elif tok.matches(TT_KEYWORD, 'lambda'):
            lambda_def = res.register(self.lambda_def())
            if res.error:
                return res
            return res.success(lambda_def)

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int,'lambda', 'func', '+', '-', '('"))

    # Parses function calls, handling function names and arguments within parentheses.
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res
        # Check for function calls
        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')', 'if','func', int, identifier, '+', '-', '(' or 'not'"))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected ',' or ')'"))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    # Parses a factor, which can be a unary operation (e.g., + or -) applied to another factor,
    # or a function call. Returns a UnaryOpNode if a unary operator is found, otherwise delegates
    # to the call method.
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        # Parse unary operations
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        return self.call()

    # Parses a term, which consists of factors connected by multiplication (*), division (/), or
    # modulo (%) operators. Utilizes the bin_op method to handle these operations.
    def term(self):
        # Parse multiplication, division, and modulo operations
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MODULO))

    # Parses an arithmetic expression consisting of terms connected by addition (+) or subtraction (-)
    # operators. Utilizes the bin_op method to handle these operations.
    def arith_expr(self):
        # Parse addition and subtraction operations
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    # Parses a comparison expression, which can be a comparison operation (e.g., ==, !=, <, >, <=, >=)
    # or a negation operation (e.g., not). Utilizes the bin_op method for comparisons and handles
    # the 'not' keyword as a unary operation.
    def comp_expr(self):
        res = ParseResult()
        # Parse unary 'not' operator
        if self.current_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EQ, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, '+', '-', '(' or 'not'"))

        return res.success(node)

    # Parses an expression consisting of comparison expressions connected by logical 'and' or 'or'
    # operators. Utilizes the bin_op method to handle these logical operations.
    def expr(self):
        res = ParseResult()
        # Parse logical 'and' and 'or' operations
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected  int, 'func', '+', '-', '(' or 'not'"))

        return res.success(node)

###################################
    # Parses a binary operation with the given functions and operators. It handles operations
    # with the specified operators, where func_a is used to parse the left operand and func_b
    # is used for the right operand if provided. If func_b is not given, func_a is used for both.
    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res
        # Parse binary operations
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
