name = "Alice"
age = 30
price = 19.99

# f-strings (recommended)
message = f"Name: {name}, Age: {age}"
formatted_price = f"Price: ${price:.2f}"

# format() method
message = "Name: {}, Age: {}".format(name, age)
message = "Name: {n}, Age: {a}".format(n=name, a=age)
