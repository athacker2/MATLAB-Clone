import re
import random

def all_vars_exist(input_line, variable_memory, function_memory):
    """Takes input for a string expression and checks whether all variables are defined. If so, it replaces all variables with their values (except matrix variables)"""
    return_line = input_line
    char_reqs = re.compile(r'[\w]')
    j = -1
    for i, char in enumerate(input_line):
        if i<j:
            continue
        if char.isalpha(): # found a variable
            j = i
            while(j < len(input_line) and char_reqs.fullmatch(input_line[j])):
                j = j + 1
            variable = input_line[i:j]
            # print("Variable:", variable)
            if not (variable in variable_memory.keys()) and not (variable in function_memory.keys()): # throw error if not a variable or function
                print("Error: Variable {variable} is not in memory.".format(variable=variable))
                return False
            elif variable in variable_memory.keys() and is_float(variable_memory[variable]): # replace value if is variable
                var_pos = return_line.find(variable)
                return_line = return_line[:var_pos] + str(variable_memory[variable]) + return_line[var_pos+len(variable):]
    return return_line

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

def is_float(x):
    if str(type(x)) == "<class 'numpy.ndarray'>":
        return False
    try:
        float(x)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def create_temp_variable(matrix, variable_memory):
    """Generates a random variable name, stores the input matrix into a dict under that name, and returns the variable name"""
    var_name = ".matrix" + str(random.randrange(1000000)) # probs replace this magic number later : P
    while var_name in variable_memory.keys():
        var_name = ".matrix" + str(random.randrange(1000000))
    variable_memory[var_name] = matrix
    return var_name