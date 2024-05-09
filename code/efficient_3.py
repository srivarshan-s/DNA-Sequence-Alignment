import sys
import time
import psutil


# Hardcoded values
DELTA = 30  # Gap penalty


# Function to return memory used by process
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


# Function to return matching penalty
def penaltyMapper(x, y):
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


# Function to build the two strings
def buildStrings(path):
    # Initialize the strings
    str_1 = ""
    str_2 = ""

    # Read the file
    with open(path, "r") as file:
        # Flag to differentiate b/w the two strings
        flag = False
        # Read the file line by line
        for line in file:
            line = line.strip()
            # First string
            if not line.isdigit() and flag == False:
                str_1 = line
                flag = True
            # Integers associated with first string
            elif line.isdigit() and flag == True:
                idx = int(line) + 1
                new_str = str_1[:idx] + str_1 + str_1[idx:]
                str_1 = new_str
            # Second string
            elif not line.isdigit() and flag == True:
                str_2 = line
                flag = False
            # Integers associated with second string
            elif line.isdigit() and flag == False:
                idx = int(line) + 1
                new_str = str_2[:idx] + str_2 + str_2[idx:]
                str_2 = new_str

    return (str_1, str_2)


# Function to perform bottom-up pass
def bottom_up(str_1, str_2):
    # Initialize the OPT matrix
    n_rows = len(str_1) + 1
    n_cols = len(str_2) + 1
    OPT = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    # Initialize first column
    for i in range(n_rows):
        OPT[i][0] = i * DELTA

    # Initialize first row
    for j in range(n_cols):
        OPT[0][j] = j * DELTA

    # Bottom-up pass
    for i in range(1, n_rows):
        for j in range(1, n_cols):
            delta_1 = OPT[i - 1][j] + DELTA  # Gap in str_1
            delta_2 = OPT[i][j - 1] + DELTA  # Gap in str_2
            # Match/Mismatch
            alpha = OPT[i - 1][j - 1] + penaltyMapper(str_1[i - 1], str_2[j - 1])
            # Set OPT val to minimum of the above 3
            OPT[i][j] = min(delta_1, delta_2, alpha)

    return OPT


# Function to perform space-efficient bottom-up pass
def eff_bottom_up(str_1, str_2):
    # Initialize the OPT matrix
    n_rows = len(str_1) + 1
    n_cols = len(str_2) + 1
    OPT = [0 for _ in range(n_rows)]

    # Initialize first column
    for i in range(n_rows):
        OPT[i] = i * DELTA

    # Bottom-up pass
    for j in range(1, n_cols):
        temp_OPT = [0 for _ in range(n_rows)]
        temp_OPT[0] = j * DELTA
        for i in range(1, n_rows):
            delta_1 = temp_OPT[i - 1] + DELTA  # Gap in str_1
            delta_2 = OPT[i] + DELTA  # Gap in str_2
            # Match/Mismatch
            alpha = OPT[i - 1] + penaltyMapper(str_1[i - 1], str_2[j - 1])
            temp_OPT[i] = min(delta_1, delta_2, alpha)
        OPT = temp_OPT

    return OPT


# Function to perform top-down pass
def top_down(str_1, str_2, OPT):
    # Top-down pass
    str_opt_1 = ""
    str_opt_2 = ""
    i_idx = len(str_1)
    j_idx = len(str_2)

    while i_idx > 0 and j_idx > 0:
        # Char in string 1 and gap in string 2
        if OPT[i_idx][j_idx] == OPT[i_idx - 1][j_idx] + DELTA:
            str_opt_1 = str_1[i_idx - 1] + str_opt_1
            str_opt_2 = "_" + str_opt_2
            i_idx -= 1
        # Char in string 2 and gap in string1
        elif OPT[i_idx][j_idx] == OPT[i_idx][j_idx - 1] + DELTA:
            str_opt_1 = "_" + str_opt_1
            str_opt_2 = str_2[j_idx - 1] + str_opt_2
            j_idx -= 1
        # Matching in string 1 and 2
        else:
            str_opt_1 = str_1[i_idx - 1] + str_opt_1
            str_opt_2 = str_2[j_idx - 1] + str_opt_2
            i_idx -= 1
            j_idx -= 1

    # Introduce gaps in string1
    while i_idx > 0:
        str_opt_1 = str_1[i_idx - 1] + str_opt_1
        str_opt_2 = "_" + str_opt_2
        i_idx -= 1

    # Introduce gaps in string2
    while j_idx > 0:
        str_opt_1 = "_" + str_opt_1
        str_opt_2 = str_2[j_idx - 1] + str_opt_2
        j_idx -= 1

    return str_opt_1, str_opt_2


# Divide and conquer function
def divide(str_1, str_2, depth):
    if not (len(str_1) <= 2 or len(str_2) <= 2):
        idx = len(str_2) // 2
        str_2_left = str_2[:idx]
        str_2_right = str_2[idx:]

        OPT_left = eff_bottom_up(str_1, str_2_left)
        OPT_right = eff_bottom_up(str_1[::-1], str_2_right[::-1])[::-1]

        min_opt_val = float("inf")
        min_idx = None

        for idx in range(len(OPT_right)):
            opt_val = OPT_left[idx] + OPT_right[idx]
            if opt_val < min_opt_val:
                min_opt_val = opt_val
                min_idx = idx

        str_1_left = str_1[:min_idx]
        str_1_right = str_1[min_idx:]

        str_1_left_opt, str_2_left_opt, opt_val_left = divide(
            str_1_left, str_2_left, depth
        )
        str_1_right_opt, str_2_right_opt, opt_val_right = divide(
            str_1_right, str_2_right, depth
        )

        str_1_opt = str_1_left_opt + str_1_right_opt
        str_2_opt = str_2_left_opt + str_2_right_opt
        opt_val = opt_val_left + opt_val_right

        return str_1_opt, str_2_opt, opt_val

    else:
        OPT = bottom_up(str_1, str_2)
        str_1_opt, str_2_opt = top_down(str_1, str_2, OPT)

        return str_1_opt, str_2_opt, OPT[len(str_1)][len(str_2)]


def main():
    # Record the start time
    start_time = time.time()

    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Error: Provide valid arguments!")
        exit()
    path: str = sys.argv[1]
    output_path: str = sys.argv[2]

    # Build the strings
    str_1, str_2 = buildStrings(path)

    # Call divide and conquer function
    str_1_opt, str_2_opt, opt_val = divide(str_1, str_2, 3)

    # Record the end time
    end_time = time.time()

    # Calculate code execution duration in ms
    exec_duration = (end_time - start_time) * 1000

    # Get memory used by process
    memory = process_memory()

    # Write to output file
    with open(output_path, "w") as file:
        file.write(str(opt_val) + "\n")
        file.write(str_1_opt + "\n")
        file.write(str_2_opt + "\n")
        file.write(str(exec_duration) + "\n")
        file.write(str(memory))


if __name__ == "__main__":
    main()
