import re
from cs50 import get_string

text = get_string("Text: ")

# count number of words by counting spaces
words = len(re.findall("[ ]", text)) + 1
# count number of letters a-z and A-Z
letters = len(re.findall("[a-zA-Z]", text))
# count number of sentences by counting ".", "!", "?"
sentences = len(re.findall("[.!?]", text))


# calculate Coleman-Liau index
# number of words in the text
W = words
# number of letters per 100 words
L = (letters / W) * 100
# number of sentences per 100 words
S = (sentences / W) * 100
index = (0.0588 * L) - (0.296 * S) - 15.8

# print the grade
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
