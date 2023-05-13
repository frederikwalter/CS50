import re


def main():
    # get input from the user with only digits in it
    while True:
        n = input("Number: ")
        if re.search("[^0-9]", n) == None and n != "":
            break
        else:
            print("Please enter a number with only digits in it")

    # check for correct pattern for each scheme and check for Luhn sum 
    if re.fullmatch("3[47]\d{13}", n) and check_luhn(int(n)):
        print("AMEX")
    elif re.fullmatch("4\d{12}(\d{3})?", n) and check_luhn(int(n)):
        print("VISA")
    elif re.fullmatch("5[1-5]\d{14}", n) and check_luhn(int(n)):
        print("MASTERCARD")
    else:
        print("INVALID")


def check_luhn(n):
    is_even = True
    sum = 0
    n = int(n)
    # iterate over entire number
    while n > 0:
        # extract every other position
        if is_even:
            sum = sum + n % 10
        else:
            # check if multiplication by 2 is larger than 10
            if (n % 10) < 5:
                sum = sum + (n % 10) * 2
            else:
                sum = sum + 1 + (((n % 10) * 2) % 10)
        n = n // 10
        is_even = not is_even
    return not (sum % 10)


main()