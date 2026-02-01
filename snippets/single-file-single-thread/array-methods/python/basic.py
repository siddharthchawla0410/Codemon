numbers = [1, 2, 3]

numbers.append(4)          # [1, 2, 3, 4]
numbers.insert(0, 0)       # [0, 1, 2, 3, 4]
numbers.pop()              # removes 4, returns it
numbers.remove(2)          # removes first occurrence of 2
length = len(numbers)      # 3
numbers.sort()             # sorts in place
numbers.reverse()          # reverses in place
