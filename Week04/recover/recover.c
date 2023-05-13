#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;


int main(int argc, char *argv[])
{
    // check if one input file is given
    if (argc != 2)
    {
        printf("Incorrent usage. Use one input argument.\n");
        return 1;
    }

    // open file and check if file exists
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Input file could not be opened.\n");
        return 1;
    }

    // define buffer
    BYTE buffer[BLOCK_SIZE];

    // counter for images
    int i = 0;

    // define file name
    char file_name[8];
    sprintf(file_name, "%i%i%i.jpg", (i % 1000) / 100, (i % 100) / 10, i % 10);

    // open file to write image
    FILE *image = fopen(file_name, "w");
    if (file == NULL)
    {
        printf("Could not create file.\n");
        return 1;
    }

    // cycle blockwise through the input file for each image
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // check if block starts with FF
        if (buffer[0] == 0xFF)
        {
            // check for remaining sequence of jpg
            if (buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] | 0x0f) == 0xef)
            {
                // close old file
                fclose(image);

                // open file to write next image
                sprintf(file_name, "%i%i%i.jpg", (i % 1000) / 100, (i % 100) / 10, i % 10);
                image = fopen(file_name, "w");
                if (file == NULL)
                {
                    printf("Could not create file.\n");
                    return 1;
                }
                i++;
            }
        }

        // write block into image file
        fwrite(buffer, 1, BLOCK_SIZE, image);
    }




    // close files
    fclose(file);
    fclose(image);

}
