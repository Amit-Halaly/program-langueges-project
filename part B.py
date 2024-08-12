from functools import reduce

# 1. Fibonacci Sequence Generator
fibonacci = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n-2), [0, 1])

# Example Usage
print("Fibonacci sequence for n=10:", fibonacci(10))

# 2. String Concatenation
concat_strings = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)

# Example Usage
strings = ["Hello", "world", "this", "is", "a", "test"]
print("Concatenated String:", concat_strings(strings))

# 3. Cumulative Sum of Squares of Even Numbers
cumulative_sum_squares = lambda lst: reduce(
    lambda acc, sublist: acc + reduce(
        lambda sub_acc, num: sub_acc + (
            (lambda n: (lambda x: x ** 2)(n))(num) if (lambda y: y % 2 == 0)(num) else 0),sublist,0),lst,0)
# Example Usage
nested_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("Cumulative Sum of Squares of Even Numbers:", cumulative_sum_squares(nested_lists))

# 4. Higher-Order Function for Binary Operations
apply_operation = lambda op: lambda seq: reduce(op, seq)

# Implementing Factorial and Exponentiation
factorial = apply_operation(lambda x, y: x * y)
exponentiation = apply_operation(lambda x, y: x ** y)

# Example Usage
print("Factorial of [1, 2, 3, 4]:", factorial([1, 2, 3, 4]))
print("Exponentiation of [2, 3]:", exponentiation([2, 3]))

# 5. Rewriting the Program Using Functional Programming
nums = [1, 2, 3, 4, 5, 6]
sum_squared = reduce(lambda acc, x: acc + x**2, filter(lambda x: x % 2 == 0, nums), 0)

# Example Usage
print("Sum of squares of even numbers:", sum_squared)

# 6. Counting Palindromes in Sublist
count_palindromes = lambda lst: list(map(lambda sublist: sum(map(lambda s: s == s[::-1], sublist)), lst))

# Example Usage
lists_of_strings = [["radar", "hello", "level"], ["world", "noon", "python"], ["madam", "racecar", "civic"]]
print("Count of palindromes in each sublist:", count_palindromes(lists_of_strings))

# 7. Lazy Evaluation Explanation
def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x

print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)

# 8. Filtering and Sorting Prime Numbers
primes_desc = lambda lst: sorted(filter(lambda x: all(x % i != 0 for i in range(2, int(x ** 0.5) + 1)), lst), reverse=True)

# Example Usage
numbers = [10, 3, 5, 7, 11, 13, 15, 20]
print("Prime numbers in descending order:", primes_desc(numbers))
