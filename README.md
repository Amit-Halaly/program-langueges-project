# BENMIT Interpreter

# Overview:
BENMIT is an interpreter for a minimalist functional programming language designed to emphasize pure functions and lambda expressions.
The language features immutability and eliminates variable assignments, promoting a purely functional approach to problem-solving.
# Create by
- @Ben-Aharoni
- @Amit-Halaly

  ### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/program-langueges-project.git
   ```

2. Open the project in your preferred IDE.

3. Compile and run the project.

### Usage

1. Run the application:

   ```bash
   py shell.py [-l] [<your file name>.ls]
   ```
- The -l flag is optional and is used to run the interpreter in line by line mode.
- The <your file name>.ls is the file you want to run, also optional. if the shell.py dosen't get any arguments, it will run in the interactive mode.
- For syntax example and Capability test, we provided test.lambda file.
   
# Data Types:
INTEGER: Represents whole numbers (e.g., -3, 0, 42).\
BOOLEAN: Represents truth values True and False.

# Operations:

# Arithmetic Operations (for INTEGERs):
Addition (+)\
Subtraction (-)\
Multiplication (*)\
Division (/)\
Modulo (%)

# Boolean Operations:
Logical AND (and)\
Logical OR (or)\
Logical NOT (!)

# Comparison Operations:
Equal to (==)\
Not equal to (!=)\
Greater than (>)\
Less than (<)\
Greater than or equal to (>=)\
Less than or equal to (<=)

# Functions:
Named Function Definitions: Define reusable functions with a given name.\
Anonymous Functions: Supports lambda expressions for creating inline, unnamed functions.\
Function Application: Apply functions to arguments to produce results.\
Recursion: Allows recursive function calls, enabling iteration-like behavior without mutable state or loops.

# Control Structures:
Recursion as Loop Replacement: Instead of traditional loops (e.g., while), recursion is used to achieve repeated execution, ensuring adherence to the language's immutability principle.

# Immutability:
Immutable Values: All values in Lam Script are immutable, ensuring that once created, they cannot be altered. This enforces a functional programming paradigm with no variable assignments or state changes.

# Error Handling:
Syntax Errors: Catches and reports invalid syntax within the code.\
Type Errors: Detects operations performed on incompatible data types.\
Runtime Errors: Identifies and handles errors that occur during the execution of the code.

#The BNF
```
expr    : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

comp-expr   : NOT comp-expr
            : arith-exper ((EE|LT|GT|LTE|GTE) arith-exper)*
call    : atom (LPAREN (expr (COMMA expr)*)? RPAREN)?

arith-exper : term ((PTUS|MINUS) term)*

term    : factor ((MUL|DIV|MODULO) factor)*

factor  : (PLUS|MINUS) factor

atom    : LPAREN expr RPAREN
        : INT
        : if-expr
        : func-def

if-expr : KEYWORD:if expr KEYWORD:then
          (KEYWORD:elif expr KEYWORD:then expr)*
          (KEYWORD:else expr)?

func-def    : KEYWORD: func IDENTIFIER?
              LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN
              ARROW expr
             |(NEWLINE statements KEYWORD:end)

statements  : NEWLINE* statement (NEWLINE+ statement)* NEWLINE*

statement	: KEYWORD:RETURN expr?
		      : KEYWORD:CONTINUE
			    : KEYWORD:BREAK
			    : expr
```

# The Main Design Decisions in the BNF Grammar:
1. Use of ; for Code Blocks
- `NEWLINE <statements>`  and `<bool_expr>` :
```
func test(x); 
    return x;
```
That said, We  want every line to end in ; .

2. Boolean Expressions
-- `<bool_expr>`:
- Boolean expressions can be composed of multiple terms, we used the `<bool_expr>` to define the base expression. That came to be when we realized That arithmetic operations uses `<Comparission expr>` as the base expression, which gives a boolean value. like in the following expression:
```(not true) or (x < 3)```

3. Short-circuit evaluation
--` <low_order_bool_op> := and | or`:
- Boolean expressions can be combined using `and` (logical AND) and `or` (logical OR). Because the language doesn't support if statements, we use of short-circuit evaluation to make conditional statements to still be possible. like in the following code:
```
func fact(n);
    (n == 0) || (n * fact(n - 1));
```

4. Function Definitions with Optional Blocks or Lite Expressions
`<func_def>`:
Functions can be defined using the def keyword, with the flexibility to include either a block of statements or a single boolean expression (using lite). This allows for both concise one-liners and more complex function definitions.
```
func add(a,b) -> a+b
```
6. Optional Elements in Function Calls and Definitions
`<call> := <atom> ( <arguments>? )?`:
Function calls and definitions allow for optional arguments and parameters, providing flexibility in how functions are written and invoked.

7. Keywords
`<keywords>`:
We decided to chnage conventional keywords. For example: lite instead of lambda to make the language more unique. but still, we kept the while is order to fit with the language design standards.
