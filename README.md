# BENMIT Interpreter

# Overview:
BENMIT is an interpreter for a minimalist functional programming language designed to emphasize pure functions and lambda expressions.
The language features immutability and eliminates variable assignments, promoting a purely functional approach to problem-solving.

# Data Types:
INTEGER: Represents whole numbers (e.g., -3, 0, 42).
BOOLEAN: Represents truth values True and False.
Operations:

# Arithmetic Operations (for INTEGERs):
Addition (+) \n
Subtraction (-)
Multiplication (*)
Division (/)
Integer division (//)
Modulo (%)

# Boolean Operations:
Logical AND (&&)
Logical OR (||)
Logical NOT (!)

# Comparison Operations:
Equal to (==)
Not equal to (!=)
Greater than (>)
Less than (<)
Greater than or equal to (>=)
Less than or equal to (<=)

# Functions:
Named Function Definitions: Define reusable functions with a given name.
Anonymous Functions: Supports lambda expressions for creating inline, unnamed functions.
Function Application: Apply functions to arguments to produce results.
Recursion: Allows recursive function calls, enabling iteration-like behavior without mutable state or loops.

# Control Structures:
Recursion as Loop Replacement: Instead of traditional loops (e.g., while), recursion is used to achieve repeated execution, ensuring adherence to the language's immutability principle.

# Immutability:
Immutable Values: All values in Lam Script are immutable, ensuring that once created, they cannot be altered. This enforces a functional programming paradigm with no variable assignments or state changes.

# Error Handling:
Syntax Errors: Catches and reports invalid syntax within the code.
Type Errors: Detects operations performed on incompatible data types.
Runtime Errors: Identifies and handles errors that occur during the execution of the code.
