#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>

bool check_luhn(long number);

int main(void)
{
    // Prompt for card number
    long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number <= 0);

    // Check if Amex
    if (number / 10000000000000 == 34 | number / 10000000000000 == 37)
    {
        if (check_luhn(number))
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // Check if MC
    else if (number / 100000000000000 > 50 & number / 100000000000000 < 56)
    {
        if (check_luhn(number))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    // Check if Visa
    else if (number / 1000000000000 == 4 | number / 1000000000000000 == 4)
    {
        if (check_luhn(number))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // catch cases with wrong length or wrong prefix
    else
    {
        printf("INVALID\n");
    }
}


// Check Luhn sum
bool check_luhn(long number)
{
    bool b = true; // indicator if even or odd position
    int sum = 0;
    while (number > 0)
    {
        // sum odd positions without multiplication
        if (b == true)
        {
            sum += (int)(number % 10);
        }
        // sum even positions with multiplication by 2
        else
        {
            // check if result after multiplication is double digit
            if (number % 10 < 5)
            {
                sum += (int)(number % 10) * 2;
            }
            else
            {
                sum += 1;
                sum += (int)((number % 10) * 2) % 10;
            }
        }
        number /= 10;
        b = !b;
    }
    return !(sum % 10);
}