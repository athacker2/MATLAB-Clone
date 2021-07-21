import sys
import numpy as np

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
    
    # Start read loop
    while True:
        input_line = input(">> ")

        # exit loop
        if(input_line == "exit"):
            break

        store_result = False
        first_var = True

        for i in range(len(input_line)):
            if input_line[i].isalpha(): # handle variables/function calls

                check for function calls (VERY BAD input handling rn lol)
                if(input_line[i:i+6] == "reduce"):
                    var_name = input_line[7:len(input_line)-1]
                    if(var_name in variable_memory):
                        row_reduce(variable_memory[var_name].copy())
                    else:
                        print("Given variable '{var_name}' is not defined.".format(var_name = var_name))
                    break
                if(input_line[i:i+3] == "mem"):
                    print(variable_memory)
                    break
                
                # read var name
                j = i
                while (j < len(input_line)) and input_line[j].isalnum():
                    j = j + 1
                var_name = input_line[i:j]

                i = j - 1 # places you on end of var_name

                #check if variable is already defined
                if var_name in variable_memory: # if yes, handle (TO DO)
                    print("Var {var_name} is defined".format(var_name = var_name))
                elif first_var: # if no, check if var is being defined (if not throw error)
                    stripped_string = input_line[j:].strip(' ')
                    if len(stripped_string) > 0 and stripped_string[0] == '=': # if not end of string and equal is next chara
                        store_result = True
                        store_var = var_name
                    else: 
                        print("Invalid input. Please enter a valid expression")
                        break
                else: # throw error since a variable can't be defined mid-expression
                    print("Given variable '{var_name}' is not defined.".format(var_name = var_name))
                    break
            
                first_var = False
                
            elif input_line[i] == '[': # handle matrix input
                matrix_string = input_line[i:input_line.find(']',i)+1]
                np_matrix = np.array(read_matrix(matrix_string))

                if store_result:
                    variable_memory[var_name] = np_matrix

                i = input_line.find(']',i) + 1
                continue

        # print(np_matrix)

# Major Cases:
# Assignment vs no-assigment
# Computation regardless of above case using order of ops.
#   1). Grouping
#   2). Mul/Div
#   3). Add/Sub

if __name__ == "__main__":
    main()