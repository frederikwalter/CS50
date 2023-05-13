#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    uint8_t average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // float one value to operate the entire calculation as float
            // after rounding store it as uint8_t as the original values
            average = round((float)(image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for filtered image
    RGBTRIPLE(*new)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (new == NULL)
    {
        printf("Not enough memory to store new image.\n");
        return;
    }

    int pixel_count;
    float sum_red;
    float sum_green;
    float sum_blue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            pixel_count = 1;
            // initialize temporary values with middle values
            sum_red = image[i][j].rgbtRed;
            sum_green = image[i][j].rgbtGreen;
            sum_blue = image[i][j].rgbtBlue;

            // top left pixel
            if (i > 0 && j > 0)
            {
                pixel_count++;
                sum_red += image[i - 1][j - 1].rgbtRed;
                sum_green += image[i - 1][j - 1].rgbtGreen;
                sum_blue += image[i - 1][j - 1].rgbtBlue;
            }
            // top middle pixel
            if (i > 0)
            {
                pixel_count++;
                sum_red += image[i - 1][j].rgbtRed;
                sum_green += image[i - 1][j].rgbtGreen;
                sum_blue += image[i - 1][j].rgbtBlue;
            }
            // top right pixel
            if (i > 0 && j < width - 1)
            {
                pixel_count++;
                sum_red += image[i - 1][j + 1].rgbtRed;
                sum_green += image[i - 1][j + 1].rgbtGreen;
                sum_blue += image[i - 1][j + 1].rgbtBlue;
            }
            // left middle pixel
            if (j > 0)
            {
                pixel_count++;
                sum_red += image[i][j - 1].rgbtRed;
                sum_green += image[i][j - 1].rgbtGreen;
                sum_blue += image[i][j - 1].rgbtBlue;
            }
            // right middle pixel
            if (j < width - 1)
            {
                pixel_count++;
                sum_red += image[i][j + 1].rgbtRed;
                sum_green += image[i][j + 1].rgbtGreen;
                sum_blue += image[i][j + 1].rgbtBlue;
            }
            // left bottom pixel
            if (i < height - 1 && j > 0)
            {
                pixel_count++;
                sum_red += image[i + 1][j - 1].rgbtRed;
                sum_green += image[i + 1][j - 1].rgbtGreen;
                sum_blue += image[i + 1][j - 1].rgbtBlue;
            }
            // bottom middle pixel
            if (i < height - 1)
            {
                pixel_count++;
                sum_red += image[i + 1][j].rgbtRed;
                sum_green += image[i + 1][j].rgbtGreen;
                sum_blue += image[i + 1][j].rgbtBlue;
            }
            // right bottom pixel
            if (i < height - 1 && j < width - 1)
            {
                pixel_count++;
                sum_red += image[i + 1][j + 1].rgbtRed;
                sum_green += image[i + 1][j + 1].rgbtGreen;
                sum_blue += image[i + 1][j + 1].rgbtBlue;
            }

            new[i][j].rgbtRed = round(sum_red / pixel_count);
            new[i][j].rgbtGreen = round(sum_green / pixel_count);
            new[i][j].rgbtBlue = round(sum_blue / pixel_count);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new[i][j];
        }
    }

    // free memory of temporary image
    free(new);

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for values of sobel filters
    RGBTRIPLE(*new)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (new == NULL)
    {
        printf("Not enough memory to store new image.\n");
        return;
    }

    float gx_red;
    float gx_green;
    float gx_blue;
    float gy_red;
    float gy_green;
    float gy_blue;
    float red;
    float green;
    float blue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initialize temporary values with middle values
            gx_red = 0;
            gx_green = 0;
            gx_blue = 0;
            gy_red = 0;
            gy_green = 0;
            gy_blue = 0;

            // top left pixel
            if (i > 0 && j > 0)
            {
                gx_red -= image[i - 1][j - 1].rgbtRed;
                gx_green -= image[i - 1][j - 1].rgbtGreen;
                gx_blue -= image[i - 1][j - 1].rgbtBlue;
                gy_red -= image[i - 1][j - 1].rgbtRed;
                gy_green -= image[i - 1][j - 1].rgbtGreen;
                gy_blue -= image[i - 1][j - 1].rgbtBlue;
            }
            // top middle pixel
            if (i > 0)
            {
                gy_red -= 2 * (float)image[i - 1][j].rgbtRed;
                gy_green -= 2 * (float)image[i - 1][j].rgbtGreen;
                gy_blue -= 2 * (float)image[i - 1][j].rgbtBlue;
            }
            // top right pixel
            if (i > 0 && j < width - 1)
            {
                gx_red += image[i - 1][j + 1].rgbtRed;
                gx_green += image[i - 1][j + 1].rgbtGreen;
                gx_blue += image[i - 1][j + 1].rgbtBlue;
                gy_red -= image[i - 1][j + 1].rgbtRed;
                gy_green -= image[i - 1][j + 1].rgbtGreen;
                gy_blue -= image[i - 1][j + 1].rgbtBlue;
            }
            // left middle pixel
            if (j > 0)
            {
                gx_red -= 2 * (float)image[i][j - 1].rgbtRed;
                gx_green -= 2 * (float)image[i][j - 1].rgbtGreen;
                gx_blue -= 2 * (float)image[i][j - 1].rgbtBlue;
            }
            // right middle pixel
            if (j < width - 1)
            {
                gx_red += 2 * (float)image[i][j + 1].rgbtRed;
                gx_green += 2 * (float)image[i][j + 1].rgbtGreen;
                gx_blue += 2 * (float)image[i][j + 1].rgbtBlue;
            }
            // left bottom pixel
            if (i < height - 1 && j > 0)
            {
                gx_red -= image[i + 1][j - 1].rgbtRed;
                gx_green -= image[i + 1][j - 1].rgbtGreen;
                gx_blue -= image[i + 1][j - 1].rgbtBlue;
                gy_red += image[i + 1][j - 1].rgbtRed;
                gy_green += image[i + 1][j - 1].rgbtGreen;
                gy_blue += image[i + 1][j - 1].rgbtBlue;
            }
            // bottom middle pixel
            if (i < height - 1)
            {
                gy_red += 2 * (float)image[i + 1][j].rgbtRed;
                gy_green += 2 * (float)image[i + 1][j].rgbtGreen;
                gy_blue += 2 * (float)image[i + 1][j].rgbtBlue;
            }
            // right bottom pixel
            if (i < height - 1 && j < width - 1)
            {
                gx_red += image[i + 1][j + 1].rgbtRed;
                gx_green += image[i + 1][j + 1].rgbtGreen;
                gx_blue += image[i + 1][j + 1].rgbtBlue;
                gy_red += image[i + 1][j + 1].rgbtRed;
                gy_green += image[i + 1][j + 1].rgbtGreen;
                gy_blue += image[i + 1][j + 1].rgbtBlue;
            }

            red = round(sqrt(pow(gx_red, 2) + pow(gy_red, 2)));
            green = round(sqrt(pow(gx_green, 2) + pow(gy_green, 2)));
            blue = round(sqrt(pow(gx_blue, 2) + pow(gy_blue, 2)));

            // cap value at 255 
            if (red < 255)
            {
                new[i][j].rgbtRed = red;
            }
            else
            {
                new[i][j].rgbtRed = 255;
            }
            if (green < 255)
            {
                new[i][j].rgbtGreen = green;
            }
            else
            {
                new[i][j].rgbtGreen = 255;
            }
            if (blue < 255)
            {
                new[i][j].rgbtBlue = blue;
            }
            else
            {
                new[i][j].rgbtBlue = 255;
            }
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new[i][j];
        }
    }

    // free memory of temporary image
    free(new);

    return;
}
