#### CONSTANTS ######

DIGITS = '0123456789'
BOOLEANVALS =['<','>' , '|' , '&','=' ,'!' , 'T', 'F']


##### ERRORS #####

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)


###### TOKENS #######

TT_INT = 'INT'
TT_TRUE = 'TRUE'
TT_FALSE = 'FALSE'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_MODULO = 'MODULO'
TT_AND = 'AND'
TT_OR = 'OR'
TT_NOT = 'NOT'
TT_EQ = 'EQ'
TT_NEQ = 'NEQ'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'


###### LEXER #####

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_token(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in BOOLEANVALS:
                tokens.append(Token(TT_TRUE))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MODULO))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(TT_LT))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(TT_GT))
                self.advance()
            elif self.current_char == '<=':
                tokens.append(Token(TT_LTE))
                self.advance()
            elif self.current_char == '>=':
                tokens.append(Token(TT_GTE))
                self.advance()
            elif self.current_char == '!=':
                tokens.append(Token(TT_NEQ))
                self.advance()
            elif self.current_char == '==':
                tokens.append(Token(TT_EQ))
                self.advance()
            elif self.current_char == '!':
                tokens.append(Token(TT_NOT))
                self.advance()
            elif self.current_char == '&&':
                tokens.append(Token(TT_AND))
                self.advance()
            elif self.current_char == '||':
                tokens.append(Token(TT_OR))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")
        return tokens, None


def make_number(self):
    num_str = ''
    while self.current_char is not None and self.current_char in DIGITS:
        num_str += self.current_char
    return Token(TT_INT, int(num_str))

def make_BOOL(self):
    if self.current_char == '>':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '=':
                return Token(TT_GTE)
        return Token(TT_GT)

    if self.current_char == '<':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '=':
                return Token(TT_LTE)
        return Token(TT_LT)

    if self.current_char == '=':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '=':
                return Token(TT_EQ)
        return None

    if self.current_char == '!':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '=':
                return Token(TT_NEQ)
        return Token(TT_NOT)

    if self.current_char == '&':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '&':
                return Token(TT_AND)
        return None

    if self.current_char == '|':
        while self.current_char is not None and self.current_char in BOOLEANVALS:
            if self.current_char == '|':
                return Token(TT_OR)
        return None

    return Token(TT_INT, int(BOOL_str))

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_token()

    return tokens, error



