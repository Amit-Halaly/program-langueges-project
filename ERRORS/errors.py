from string_with_arrows import *


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start  # Starting position of the error
        self.pos_end = pos_end  # Ending position of the error
        self.error_name = error_name    # Name of the error
        self.details = details  # Details about the error

    # Returns a formatted string representation of the error, including the error name,
    # details, and a visual representation of the error location in the source code.
    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        # Initializes the IllegalCharError with a specific error name and details.
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        # Initializes the ExpectedCharError with a specific error name and details.
        super().__init__(pos_start, pos_end, 'Expected Character',details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        # Initializes the InvalidSyntaxError with a specific error name and optional details.
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        # Initializes the RTError with a specific error name, details, and execution context.
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context  # The context in which the error occurred

    # Returns a formatted string representation of the runtime error, including a traceback
    # of the call stack, the error name, details, and a visual representation of the error location.
    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    # Generates a traceback of the call stack showing the sequence of function calls leading to the error.
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


# POSITION ######
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx    # Character index in the file
        self.ln = ln    # Line number in the file
        self.col = col   # Column number in the line
        self.fn = fn    # File name
        self.ftxt = ftxt     # File text (source code)

    # Advances the position by one character, updating line and column numbers as needed.
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    # Creates a copy of the current position.
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
