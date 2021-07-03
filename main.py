import sys
import numpy as np

# line = input(">> ")
rows = input("Please input number of rows: ")
cols = input("Please input number of cols: ")
print("Please input the matrix you would like to find the fundamental subspaces of.")
input_matrix = input(">> ")

# parse the input matrix (assume MATLAB notation)
#improve later

matrix = np.zeros((int(rows),int(cols)))
currRow = 0
currCol = 0
for chara in input_matrix:
    if chara.isdigit():
        print(chara)
        matrix[currRow][currCol] = float(chara)
        currCol = currCol + 1
    elif chara == ";":
        currRow = currRow + 1
        currCol = 0

for i in range(rows):
    for j in range(cols):
        print(matrix[i][j])