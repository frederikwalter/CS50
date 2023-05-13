from cs50 import get_int


# promt user for height of the pyramid
while True:
    h = get_int("Height: ")
    if 0 < h < 9:
        break
    else:
        print("The height should be between 1 and 8")

# build pyramid
for i in range(h):
    print((" " * (h - i - 1)) + ("#" * (i + 1)) + "  " + "#" * (i + 1))

