str1 = "_A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G"
str2 = "TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG"

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

opt_val = 0

for i in range(len(str1)):
    if str1[i] == "_" or str2[i] == "_":
        opt_val += 30
    else:
        opt_val += alpha(str1[i], str2[i])

print(opt_val)
