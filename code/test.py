import sys


def alpha(x, y):
    char_map = {
        "A": 0,
        "C": 1,
        "G": 2,
        "T": 3,
    }
    alpha_matrix = [
        [0, 110, 48, 94],
        [110, 0, 118, 48],
        [48, 118, 0, 110],
        [94, 48, 110, 0],
    ]
    return alpha_matrix[char_map[x]][char_map[y]]


def main():
    # Parse command line arguments
    if len(sys.argv) != 2:
        print("Error: Provide valid arguments!")
        exit()
    path: str = sys.argv[1]

    # Define variables
    opt_val1 = 0
    opt_val2 = 0
    str1 = ""
    str2 = ""

    # Read the optimal value and aligned strings
    with open(path, "r") as file:
        line = file.readline().strip()
        opt_val1 = int(line)
        str1 = file.readline().strip()
        str2 = file.readline().strip()

    for i in range(len(str1)):
        if str1[i] == "_" or str2[i] == "_":
            opt_val2 += 30
        else:
            opt_val2 += alpha(str1[i], str2[i])

    if opt_val1 == opt_val2:
        print(path, "passed test")
    else:
        print("Error:", path, "failed test!")


if __name__ == "__main__":
    main()
