text = "Hello, World!"

# Case methods
upper = text.upper()       # "HELLO, WORLD!"
lower = text.lower()       # "hello, world!"
title = text.title()       # "Hello, World!"

# Search methods
index = text.find("World")     # 7 (-1 if not found)
contains = "World" in text     # True
starts = text.startswith("Hello")  # True
ends = text.endswith("!")      # True

# Manipulation methods
replaced = text.replace("World", "Python")  # "Hello, Python!"
stripped = "  text  ".strip()   # "text"
split_list = text.split(", ")   # ["Hello", "World!"]
joined = "-".join(["a", "b"])   # "a-b"

# Character checks
"abc".isalpha()   # True
"123".isdigit()   # True
"abc123".isalnum()  # True
