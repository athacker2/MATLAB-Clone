import numpy as np

def swap_rows(input_matrix, i, j):
    """Helper functionn that swaps matrix rows"""
    temp_row = np.array(input_matrix[i,:])
    input_matrix[i,:] = input_matrix[j,:]
    input_matrix[j,:] = temp_row
    return input_matrix

def row_reduce(input_matrix):
    """Reduces a matrix to reduced row echelon form"""
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
    return True, input_matrix

def create_identity(n):
    """Creates an nxn identity matrix"""
    if int(n) != n:
        print("Error: Invalid Identity Dimension")
        return False, ""
    return True, np.eye(int(n))

def find_eigenvalues(input_matrix):
    """Finds Eigenvalues of a given matrix (currently restricted to 2x2)"""
    matrix_size = input_matrix.shape
    if(matrix_size[0] != matrix_size[1]):
        print("Error: Can't find eigenvalues of non-square matrix")
        return False, ""
    if(matrix_size[0] != matrix_size[1]):
        print("Error: Can only compute eigenvalues of 2x2 matrix (TBI)")
        return False, ""
    
    # edge case: 1x1 matrix
    if(matrix_size[1] == 1):
        return True, float(input_matrix)

    x_1 = input_matrix[0][0] + input_matrix[1][1]
    x_2 = determinant(input_matrix)[1]

    if(x_1 + pow(x_1,2) - 4 * x_2 < 0):
        print("No Eigenvalues")
        return False, ""

    eigenvalues = list()
    eigenvalues.append( (x_1 + pow(pow(x_1,2) - 4 * x_2,0.5)) / (2))
    eigenvalues.append( (x_1 - pow(pow(x_1,2) - 4 * x_2,0.5)) / (2))

    return True, eigenvalues

def classifical_gram_schmidt(input_matrix):
    # find basis for input matrix
    matrix_size = input_matrix.shape
    reduced_matrix = row_reduce(input_matrix.copy())[1]

    currRow = 0
    basis_cols_ind = list()
    for i in range(matrix_size[1]):
        if(reduced_matrix[currRow][i] != 0):
            basis_cols_ind.append(i)
            currRow += 1
            if(currRow >= matrix_size[0]):
                break
    basis_cols = [input_matrix[:,i] for i in basis_cols_ind]
    
    # apply cgs algorithm
    # print(basis_cols)

    q_vecs = list()
    r_vecs = list()
    col_size = basis_cols[0].shape[0]

    for vector in basis_cols:
        projection_vecs = list()
        r_vec = list()
        for q_vec in q_vecs:
            r_val = q_vec.transpose() @ vector
            proj_vec = r_val * q_vec
            projection_vecs.append(proj_vec)
            r_vec.append(r_val)
        for proj_vec in projection_vecs:
            vector -= proj_vec
        
        r_vec.append(pow(vector.transpose() @ vector,0.5))
        vector /= pow(vector.transpose() @ vector,0.5)
        while(len(r_vec) < col_size):
            r_vec.append(0)
        
        r_vecs.append(r_vec)
        q_vecs.append(vector)

    r_matrix = np.array(r_vecs).transpose()
    q_matrix = np.array(q_vecs)
    print("Q Matrix: \n {q}".format(q = q_matrix))
    print("R Matrix: \n {r}".format(r = r_matrix))

    return True, np.concatenate((q_matrix,r_matrix),axis=1)

# A = [12 -51 4; 6 167 -68; -4 24 -41]

def modified_gram_schmidt(input_matrix):
    # find basis for input matrix
    matrix_size = input_matrix.shape
    reduced_matrix = row_reduce(input_matrix.copy())[1]

    currRow = 0
    basis_cols_ind = list()
    for i in range(matrix_size[1]):
        if(reduced_matrix[currRow][i] != 0):
            basis_cols_ind.append(i)
            currRow += 1
            if(currRow >= matrix_size[0]):
                break
    basis_cols = [input_matrix[:,i] for i in basis_cols_ind]

    # apply mgs algorithm

    q_vecs = list()
    r_vecs = list()

    for i in range(len(basis_cols)):
        r_vec = list()

        for j in range(i):
            r_vec.append(0)

        vector = basis_cols[i]

        #normalize
        r_vec.append(pow(vector.transpose() @ vector,0.5))
        vector /= pow(vector.transpose() @ vector,0.5)

        q_vecs.append(vector)

        # project out of remaining set
        for j in range(i+1,len(basis_cols)):
            r_val = vector.transpose() @ basis_cols[j]
            r_vec.append(r_val)
            basis_cols[j] -= r_val*vector
        
        r_vecs.append(r_vec)

    r_matrix = np.array(r_vecs)
    q_matrix = np.array(q_vecs)
    print("Q Matrix: \n {q}".format(q = q_matrix))
    print("R Matrix: \n {r}".format(r = r_matrix))

    return True, np.concatenate((q_matrix,r_matrix),axis=1)

def householder_triangularization(input_matrix):
    # find basis for input matrix
    matrix_size = input_matrix.shape
    reduced_matrix = row_reduce(input_matrix.copy())[1]

    currRow = 0
    basis_cols_ind = list()
    for i in range(matrix_size[1]):
        if(reduced_matrix[currRow][i] != 0):
            basis_cols_ind.append(i)
            currRow += 1
            if(currRow >= matrix_size[0]):
                break

    basis_cols = [input_matrix[:,i] for i in basis_cols_ind]
    col_size = basis_cols[0].shape[0]
    Q = np.eye(col_size)

    for k in range(len(basis_cols)):
        e = np.zeros(len(basis_cols) - k)
        e[0] = 1

        x = input_matrix[k:,k]
        v = (-1*pow(x.transpose() @ x,0.5) if x[0] < 0 else pow(x.transpose() @ x,0.5)) * e + x

        v = v[:,np.newaxis]
        P = (v @ v.transpose()) * (1/(v.transpose() @ v))
        F = np.eye(len(basis_cols)-k) - 2 * P

        I_temp = np.eye(k)
        Z_temp = np.zeros((col_size-k,k))
        Z_temp2 = np.zeros((k,col_size-k))

        Q_k = np.concatenate((np.concatenate((I_temp,Z_temp),axis=0),np.concatenate((Z_temp2,F),axis=0)),axis=1)
        input_matrix = Q_k @ input_matrix

        print("Q Matrix: \n {q}".format(q = Q_k))
        print("Input Matrix: \n {r}".format(r = input_matrix))

        Q = Q @ Q_k.transpose()

    print("Q Matrix: \n {q}".format(q = Q))
    print("R Matrix: \n {r}".format(r = input_matrix))

    return True,np.concatenate((Q,input_matrix),axis=1)

def givens_rotation():
    print("TBI")

def singular_value_decomp():
    print("TBI")

def test_function(x):
    return 12

def determinant(input_matrix):
    """Finds determinant of input matrix"""
    matrix_size = input_matrix.shape
    if(matrix_size[0] != matrix_size[1]):
        print("Error: Can't find determinant of non-square matrix")
        return False, ""

    # base case 1x1
    if(matrix_size[0] == 1):
        return True, float(input_matrix)

    # base case 2x2
    if(matrix_size[0] == 2):
        return True, float(input_matrix[0][0] * input_matrix[1][1] - input_matrix[0][1] * input_matrix[1][0])
    

    input_matrix = row_reduce(input_matrix)[1]

    # find row/col w/most zeros
    max_row_ct = -1
    max_row = 0
    for i in range(matrix_size[0]): # rows
        zero_ct = 0
        for j in range(matrix_size[1]): # col
            if(input_matrix[i][j] == 0):
                zero_ct += 1
        if(zero_ct > max_row_ct) :
            max_row_ct = zero_ct
            max_row = i
    
    
    max_col_ct = -1
    max_col = 0
    for i in range(matrix_size[1]): # col
        zero_ct = 0
        for j in range(matrix_size[0]): # row
            if(input_matrix[j][i] == 0):
                zero_ct += 1
        if(zero_ct > max_col_ct) :
            max_col_ct = zero_ct
            max_col = i
    
    
    if max_row_ct > max_col_ct: # choose row
        det = 0
        for i in range(matrix_size[1]): # col
            currOp = pow(-1,i)
            if input_matrix[max_row][i] != 0:
                matrix_copy = np.delete(input_matrix, max_row, 0)
                matrix_copy = np.delete(matrix_copy, i, 1)
                det += input_matrix[max_row][i] * determinant(matrix_copy)[1] * currOp
    else: # choose col
        det = 0
        for i in range(matrix_size[0]): # row
            if input_matrix[i][max_col] != 0:
                currOp = pow(-1,i)
                matrix_copy = np.delete(input_matrix, i, 0)
                matrix_copy = np.delete(matrix_copy, max_col, 1)
                det += input_matrix[i][max_col] * determinant(matrix_copy)[1] * currOp

    return True, float(det)

