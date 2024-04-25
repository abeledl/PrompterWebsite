def create_pattern(length):
    pattern = []
    twoZero = True
    firstPosition = 0
    if length % 2 == 0:
        firstPosition = int(length / 2) - 2
    else:
        firstPosition = int((length + 1) / 2) - 2
        twoZero = False 
    if length == 1:
        pattern.append(firstPosition)   
    if length == 2:
        for _ in range(2):
            pattern.append(firstPosition)   
    if length == 3:
        for _ in range(3):
            pattern.append(firstPosition)   
    if length > 3:
        for _ in range(4):
            pattern.append(firstPosition)   
    if length > 4:
        # Pattern for even numbers
        if twoZero:
            for i in range(int(firstPosition) - 1, 0, -1):
                pattern.append(i)
                pattern.append(i)
            pattern.append(0)
            pattern.append(0)
        else: 
            for i in range(int(firstPosition) -1, 0, -1):
                pattern.append(i)
                pattern.append(i)
            pattern.append(0)
    return pattern

length = 8
pattern_array = create_pattern(length)

# Print the resulting array
print(pattern_array, len(pattern_array))
