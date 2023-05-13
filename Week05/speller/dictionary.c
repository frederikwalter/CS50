// Implements a dictionary's functionality

#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// counter for number of words in the dictionary
unsigned int size_dict = 0;

void free_node(node *n);
void init_node(node *n);


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_value = hash(word);
    node *ptr = table[hash_value];
    while (ptr != NULL)
    {
        if (!strcasecmp(ptr->word, word))
        {
            return true;
        }
        ptr = ptr->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int value = 5381;
    int i = 0;

    while (word[i] != '\0')
    {
        value = ((value << 5) + value) + word[i];
        i++;
    }

    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // initialize hash table
    for (int i = 0; i < 5; i++)
    {
        table[i] = NULL;
    }

    // open file and check if memory can be allocated
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Could not allocate memory to open dictionary\n");
        return false;
    }

    // loop through dictionary and find words separated by '\n' and add them to a new node in the hash table
    char c;
    node *n = malloc(sizeof(node));
    init_node(n);


    int i = 0;
    int hash_value;
    while (fread(&c, sizeof(char), 1, dict))
    {
        if (c != '\n')
        {
            n->word[i] = c;
            i++;
        }
        else
        {
            // if word found store string, add node to table and create a new node
            n->word[i] = '\0';
            hash_value = hash(n->word);
            n->next = table[hash_value];
            table[hash_value] = n;
            n = malloc(sizeof(node));
            init_node(n);
            size_dict++;
            i = 0;
        }
    }
    // free the node from the last iteration
    free(n);
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return size_dict;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *ptr;
    for (int i = 0; i < N; i++)
    {
        ptr = table[i];
        if (ptr != NULL)
        {
            free_node(ptr);
        }
    }
    return true;
}

void free_node(node *n)
{
    if (n->next == NULL)
    {
        free(n);
    }
    else
    {
        free_node(n->next);
        free(n);
    }
    return;
}

void init_node(node *n)
{
    if (n == NULL)
    {
        printf("Could not create new node");
        return;
    }

    // initialize node with NUL and NULL
    for (int i = 0; i < LENGTH + 1; i++)
    {
        n->word[i] = '\0';
    }
    n->next = NULL;
}