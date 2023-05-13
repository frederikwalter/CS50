#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt for input
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 | h > 8);

    // build pyramid  of blocks
    for (int i = 0; i < h; i++)
    {
        // left side of the pyramid
        for (int j = 0; j < h; j++)
        {
            if (j + i < h - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }

        // space in between the pyramid
        printf("  ");


        // right side of the pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}