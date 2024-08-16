import benmit

while True:
    text = input('benmit ->')
    result, error = benmit.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        print(result)