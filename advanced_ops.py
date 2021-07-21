def row_reduce(input_matrix):
    matrix_size = input_matrix.shape
    print(input_matrix)
    # current issue: subsitution starts at top left and bottom right. BUT in the case of solving Ax = b, for example, in back substitution i want to leave augmented column alone since it isn't pibot column.
    # solution: for both forward and backwards, start eliminating up/down at the PIVOT. if the pivot is not at (i,i) then do row swaps to make pivot at that position.
    # implentation:
    #   1). iterate through cols
    #   2). for forward sub, find the leftmost element that is closest to top (usually this will be (0,0)) and do row swaps to make it current row.
    #   3). eliminate downn
    #   4). continue this process for each column

    # forward elimination
    for i in range(matrix_size[1]): # cols
        for j in range(i+1, matrix_size[0], 1): # rows
            if(i < j and input_matrix[j,i] != 0): # only eliminate elements in lower half if not 0
                input_matrix[j, :] = input_matrix[j, :] - input_matrix[i, :]*input_matrix[j,i]/input_matrix[i,i]
                print("Eliminted: ({j},{i})".format(i = i, j = j))
                print(input_matrix)
    
    print("Forwards")
    for i in reversed(range(matrix_size[1])): # cols
        for j in range(matrix_size[0]-1-i,-1,-1): # rows
            if(i > j and input_matrix[j,i] != 0):
                input_matrix[j, :] = input_matrix[j, :] - input_matrix[i, :]*input_matrix[j,i]/input_matrix[i,i]
                print("Eliminted: ({i},{j})".format(i = i, j = j))
                print(input_matrix)


    