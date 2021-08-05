import numpy as np

def scalar_mult():
    print(2)

def swap_rows(input_matrix, i, j):
    temp_row = np.array(input_matrix[i,:])
    input_matrix[i,:] = input_matrix[j,:]
    input_matrix[j,:] = temp_row
    return input_matrix

def add_mult():
    print(3)
