day = 3
match day:
    case 1:
        name = "Monday"
    case 2:
        name = "Tuesday"
    case 3:
        name = "Wednesday"
    case _:
        name = "Unknown"
print(name)  # "Wednesday"
