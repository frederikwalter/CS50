#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // ask for the name
    string name = get_string("What's your name? ");

    // greet the user by name
    printf("hello, %s\n", name);
}