import numpy as np

#terminator must be a non-alphanumeric character
terminator = "#"

### BUILDING BWT
def add_termination(sequence):
    #Add the termination symbol to the original string
    sequence = sequence
    sequence += terminator

    return sequence

def sorting_key():
    #Define the new alphabet and the respective index dictionary
    alphabet = f"{terminator}ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sorting_key = dict(zip(alphabet, range(len(alphabet))))

    return sorting_key

def sort_suffix_list(suffix_list):
    key = sorting_key()
    #sort the list of tuples containing all suffixes and their indexes
    suffix_list = list(sorted(suffix_list, key=lambda word: [key[c] for c in word[1].upper()]))

    return suffix_list

def build_suffix_array(sequence):

    sequence = add_termination(sequence)
    suffix_list = []

    #to keep track of indexes and suffixes
    for i in range(len(sequence)):
        suffix_list.append((i, sequence[i:]))

    suffix_list = sort_suffix_list(suffix_list)

    #array containing only the indexes
    suffix_array = np.array([i[0] for i in suffix_list])

    return suffix_array

def BWT(sequence):
    suffix_array = build_suffix_array(sequence)
    bwt = ""

    #loop through the suffix array and compute the BWT
    for i in suffix_array:
        if i == 0:
            bwt += terminator
        else:
            bwt += sequence[i-1]

    return bwt

### REVERSING BWT
def get_FL_column(bwt):
    key = sorting_key()
    #get F column from sorting bwt and L column from bwt
    F_column = np.array(list(sorted([i for i in bwt], key=lambda word: [key[c] for c in word.upper()])))
    L_column = np.array([i for i in bwt])
    return F_column, L_column

def rank_column(column):
    counter = dict()
    ranked = np.empty(len(column), dtype=object)

    for i, j in enumerate(column):
        if j not in counter:
            ranked[i] = (j, 0)
            counter[j] = 1
        else:
            ranked[i] = (j, counter[j])
            counter[j] += 1

    return ranked

def reverse_BWT(bwt):
    F_column, L_column = get_FL_column(bwt)
    F_column = rank_column(F_column)
    L_column = rank_column(L_column)
    reversed = terminator

    idx = 0
    last_idx = 0
    initialization = True

    for i in range(len(L_column)):
        #It computes the cumulative counter, here called index; in the initialization step It just puts the first character
        #of L_column at the end of the string before the termination
        while L_column[last_idx] != F_column[idx]:
            if idx == 0 and initialization is True:
                reversed = L_column[idx][0] + reversed
                initialization = False
            idx += 1
        #Storing the last_idx is needed to jump in the L_column at the next iteration of the for loop
        last_idx = idx
        #It only adds a character if it is different from # and It breaks the loop otherwise because it recomposed the
        #original word
        if L_column[idx][0] != terminator:
            reversed = L_column[idx][0] + reversed
        else:
            break
        idx = 0

    return reversed

#testing code
if __name__ == "__main__":
    sequence = "precipitevolissimevolmente"
    transformed = BWT(sequence)
    print(transformed)
    reversed = reverse_BWT(transformed)
    print(reversed)