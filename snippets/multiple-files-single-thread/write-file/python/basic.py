# Write to file (creates or overwrites)
with open("file.txt", "w") as file:
    file.write("Hello, World!")

# Append to file
with open("file.txt", "a") as file:
    file.write("\nNew line")

# Write multiple lines
lines = ["Line 1", "Line 2", "Line 3"]
with open("file.txt", "w") as file:
    file.writelines(line + "\n" for line in lines)
