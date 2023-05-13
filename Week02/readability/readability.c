#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{
    // get input from user
    string text = get_string("Text: ");

    // calculate Coleman-Liau index
    float W = (float) count_words(text); // number of words in the text
    float L = (float) count_letters(text) / W * 100; // number of letters per 100 words
    float S = (float) count_sentences(text) / W * 100; // number of sentences per 100 words
    float index = (0.0588 * L) - (0.296 * S) - 15.8;

    // print the grade
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

// count number of letters in the text
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // check if character is alphabetic
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// count number of words in the text
int count_words(string text)
{
    int words = 1; // there will be one word more than spaces and at least one word
    for (int i = 0; i < strlen(text); i++)
    {
        // check if character is space, tab or new line
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

// count number of sentences
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // check if character is '.', '?' or '!'
        if (text[i] == '.' | text[i] == '?' | text[i] == '!')
        {
            sentences++;
        }
    }
    return sentences;
}