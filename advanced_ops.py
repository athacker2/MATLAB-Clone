from row_ops import *

def row_reduce(input_matrix):
    matrix_size = input_matrix.shape
    # forward elimination
    top_row = 0
    for i in range(matrix_size[1]): # cols
        for j in range(top_row,matrix_size[0]): # rows
            if input_matrix[j, i] != 0: # found non-zero entry
                swap_rows(input_matrix, j, top_row)
                for k in range(top_row+1,matrix_size[0]):
                    input_matrix[k,:] = input_matrix[k,:] - input_matrix[top_row,:]*input_matrix[k,i]/input_matrix[top_row,i]
                top_row = top_row + 1
                break
            else:
                continue
    # back substitution
    leftmost_col = matrix_size[1]
    for j in reversed(range(matrix_size[0]-1)): # rows
        for i in range(0,leftmost_col): # cols
            if input_matrix[j,i] != 0: # found non-zero row (pivot)
                input_matrix[j,:] = input_matrix[j,:]*1/input_matrix[j,i]
                for k in range(0,j):
                    input_matrix[k,:] = input_matrix[k,:] - input_matrix[j,:]*input_matrix[k,i]
                leftmost_col = i - 1
                break
            else:
                continue
    return input_matrix

def test_function(x):
    return 12

function_memory = {
    "test_func": test_function,
    "rref": row_reduce
}