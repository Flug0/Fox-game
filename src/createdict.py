

index = int(input("Enter starting index: "))

while True:
    x, y = input().split(maxsplit=1)
    y = y.split()

    for elem in y:
        print(f"{index} : ({x}, {elem}), ", end="")
        index += 1
