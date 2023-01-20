# This function load dictionary from file and return a set for O(1) search and insert
def load_dictionary():
    dictionary = set()
    with open('res/words.txt') as f:
        for line in f:
            dictionary.add(line.strip())
    return dictionary


# This function compute distance between s1 and s2, cost are equals for all operations
def edit_dp(s1, s2):
    len1 = len(s1)
    len2 = len(s2)

    # Initialize matrix of distances
    dp = [[0 for i in range(len2 + 1)]
          for j in range(len1 + 1)]

    # Fill with max value
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    # Compute the distance matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):

            # If the characters are same
            # no changes required
            if s2[j - 1] == s1[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            # Minimum of four operations possible (insert, replace, delete, anagram)
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],
                                   dp[i - 1][j - 1],
                                   dp[i - 1][j])
                # transposition
                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

    return dp


# This function print sum of every operation for go from s1 to s2
def print_summary_of_changes(s1, s2, dp):
    i = len(s1)
    j = len(s2)
    replace = 0
    add = 0
    delete = 0
    anagrams = 0
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            replace += 1
            j -= 1
            i -= 1
        elif dp[i][j] == dp[i - 1][j] + 1:
            delete += 1
            i -= 1
        elif dp[i][j] == dp[i][j - 1] + 1:
            add += 1
            j -= 1
        elif dp[i][j] == dp[i - 2][j - 2] + 1:
            anagrams += 1
            i -= 2
            j -= 2
    print()
    print("Sostituzioni: " + str(replace) + ", Aggiunte: " + str(add) + ", Cancellazioni: " +
          str(delete) + ", Anagrammi: " + str(anagrams))


# This function print well-formed path from s1 to s2
def print_path(s1, s2, dp):
    dictionary = load_dictionary()
    i = len(s1)
    j = len(s2)
    before_word = s1

    print()
    print("Cammino migliore:")
    print(s1, end="")
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            if s1[0:i - 1] + s2[j - 1] + s1[i:len(s1)] in dictionary:
                print(" -> " + s1[0:i - 1] + s2[j - 1] + s1[i:len(s1)], end="")
                before_word = s1[0:i - 1] + s2[j - 1] + s1[i:len(s1)]

            j -= 1
            i -= 1
        elif dp[i][j] == dp[i - 1][j] + 1:
            if s1[0:i - 1] + s1[i:len(s1)] in dictionary:
                print(" -> " + s1[0:i - 1] + s1[i:len(s1)], end="")
                before_word = s1[0:i - 1] + s1[i:len(s1)]

            i -= 1
        elif dp[i][j] == dp[i][j - 1] + 1:
            if s1[0:i] + s2[j - 1] + s1[i:len(s1)] in dictionary:
                print(" -> " + s1[0:i] + s2[j - 1] + s1[i:len(s1)], end="")
                before_word = s1[0:i] + s2[j - 1] + s1[i:len(s1)]

            j -= 1
        elif dp[i][j] == dp[i - 2][j - 2] + 1:
            if s1[0:i - 2] + s1[i - 1] + s1[i - 2] + s1[i:len(s1)] in dictionary:
                print(" -> " + s1[0:i - 2] + s1[i - 1] + s1[i - 2] + s1[i:len(s1)], end="")
                before_word = s1[0:i - 2] + s1[i - 1] + s1[i - 2] + s1[i:len(s1)]

            i -= 2
            j -= 2

    if s2 != before_word:
        print(" -> " + s2)


# This function print details about every operation for go from s1 to s2
def print_detailed_changes(s1, s2, distance_matr):
    i = len(s1)
    j = len(s2)

    print()
    print("Dettaglio delle modifiche: (leggere da destra verso sinistra)")
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            i -= 1
            j -= 1
        elif distance_matr[i][j] == distance_matr[i - 1][j - 1] + 1:
            print("Sostituzione " + s1[i - 1] + " con " + s2[j - 1])
            j -= 1
            i -= 1
        elif distance_matr[i][j] == distance_matr[i - 1][j] + 1:
            print("Cancellazione " + s1[i - 1])
            i -= 1
        elif distance_matr[i][j] == distance_matr[i][j - 1] + 1:
            print("Aggiunta " + s2[j - 1])
            j -= 1
        elif distance_matr[i][j] == distance_matr[i - 2][j - 2] + 1:
            print("Anagramma " + s1[i - 2] + s1[i - 1])
            i -= 2
            j -= 2


def main():
    s1 = input("Inserisci la prima parola: ")
    s2 = input("Inserisci la seconda parola: ")

    print_detailed_output = input("Vuoi stampare l'output dettagliato di ogni cambiamento effettuato? (s/n): ")
    if print_detailed_output == "s":
        print_detailed_output = True

    distance_matr = edit_dp(s1, s2)
    print_path(s1, s2, distance_matr)
    print_summary_of_changes(s1, s2, distance_matr)
    if print_detailed_output is True:
        print_detailed_changes(s1, s2, distance_matr)


if __name__ == "__main__":
    main()
