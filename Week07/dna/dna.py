import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Please input a CSV file as first command-line argument and a TXT file with the sequence as the second argument")
        return 1

    # Read database file into a variable
    database = []
    with open(sys.argv[1]) as file:
        file_reader = csv.DictReader(file)
        for p in file_reader:
            database.append(p)

    # Get Short Tandem Repeats (STRs) of the database
    dna_STRs = list(database[1].keys())[1:]

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    test = {}
    for subsequence in dna_STRs:
        test[subsequence] = longest_match(sequence, subsequence)

    # Check database for matching profiles
    for p in database:
        for s in dna_STRs:
            if int(p[s]) != test[s]:
                break
            elif s == dna_STRs[len(dna_STRs) - 1]:
                print(f"{p['name']}")
                return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
