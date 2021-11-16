import re
import random
import numpy as np

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
            if not (variable_memory.contains_var(variable)) and not (variable in function_memory.keys()): # throw error if not a variable or function
                print("Error: Variable {variable} is not in memory.".format(variable=variable))
                return False
            elif variable_memory.contains_var(variable) and is_float(variable_memory.get_value(variable)): # replace value if is variable
                var_pos = return_line.find(variable)
                return_line = return_line[:var_pos] + str(variable_memory.get_value(variable)) + return_line[var_pos+len(variable):]
    return return_line

def read_matrix(matrix_string):
    """Takes input for a string that is a MATLAB-formatted matrix and converts it to an numpy matrix"""
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
    return np.array(matrix_nums)

def is_float(x):
    """Verifies whether an input is a float or not (used to distinguish matrices and floats)"""
    # since 1x1 matrices can be converted to floats
    if str(type(x)) == "<class 'numpy.ndarray'>":
        return False
    try:
        float(x)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def is_function(input_line, first_open, function_memory):
    """Takes input for a user command and position of first open parenthsis and checks if it corresponds to a function call. Returns corresponding function and new open pos if so."""
    char_reqs = re.compile(r'[\w]')
    j = first_open-1
    while j >= 0 and char_reqs.fullmatch(input_line[j]):
        j = j - 1
    variable = input_line[j+1:first_open].strip()
    if variable in function_memory.keys():
        return function_memory[variable], j+1
    return False, 0