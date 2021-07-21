import sys
import numpy as np
import re

from advanced_ops import *

def read_matrix(matrix_string):
    matrix_nums = list()
    current_row = list()
    
    end_index = -1
    for i in range(len(matrix_string)):
        if i < end_index:
            continue
        chara = matrix_string[i]
        if chara.isdigit() or chara == '-':
            end_index = min({matrix_string.find(" ",i) if matrix_string.find(" ",i) != -1 else len(matrix_string), matrix_string.find(";",i) if matrix_string.find(";",i) != -1 else len(matrix_string), len(matrix_string)-1})
            current_row.append(float(matrix_string[i:end_index]))
        elif chara == ';' or chara == ']':
            matrix_nums.append(current_row.copy())
            current_row.clear()
        else:
            continue
    return matrix_nums


def main():
# create memory to store values
    variable_memory = dict()

# create regex for valid var names
    variable_format = re.compile(r'[^\W\d_]+[^\W]*')
    
# Start read loop
    while True:
        input_line = input(">> ")

    # exit loop
        if(input_line == "exit"):
            break

    # identify if we are storing result or not
        store_result = True if input_line.find('=') != -1 else False
    # if we're storing the result, identify the variable name
        if store_result:
            var_name = input_line[:input_line.find('=')].strip()
            print(var_name)
        # if the variable name isn't valid throw error
            if(not variable_format.fullmatch(var_name)):
                print("Invalid Variable Name : {var_name}".format(var_name=var_name))
                continue
        # update the input line to only contain the expression to evaluate now
            input_line = input_line[input_line.find('=')+1:].strip()
            print(input_line)

        # iterate through the string and simplify it one step at a time following PEMDAS + replace computations as you go + error handle as you go
        for i, char in enumerate(input_line):
            print(char)
            


# Major Cases:
# Assignment vs no-assigment
# Computation regardless of above case using order of ops.
#   1). Grouping
#   2). Mul/Div
#   3). Add/Sub

if __name__ == "__main__":
    main()