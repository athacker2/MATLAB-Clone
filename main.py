import sys
import numpy as np
import re
import random

from advanced_ops import *
from input_handling import *
from expressions import *

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

def clean_memory(variable_memory):
    """Clears all temporary matrices from memory created during computation of expression"""
    delete = [key for key in variable_memory if key[0:7] == ".matrix"]
    for key in delete: del variable_memory[key]

def read_loop(variable_memory):
    # create regex for valid var names
    variable_format = re.compile(r'[^\W\d_]+[^\W]*')

    input_line = input(">> ")

    # exit loop
    if(input_line == "exit"):
        return False

    if(input_line == 'mem'):
        print(variable_memory)
        print(function_memory)
        return True

    # identify if we are storing result or not
    store_result = True if input_line.find('=') != -1 else False

    # if we're storing the result, identify the variable name
    if store_result:
        var_name = input_line[:input_line.find('=')].strip()
        # print(var_name)
        # if the variable name isn't valid throw error
        if(not variable_format.fullmatch(var_name)):
            print("Error: Invalid Variable Name '{var_name}'".format(var_name=var_name))
            return True
        # update the input line to only contain the expression to evaluate now
        input_line = input_line[input_line.find('=')+1:].strip()
        # print("Expression:", input_line)

    # ensure all variables used in expression are defined, else throw error, replace vars w/vals if all exist
    input_line = all_vars_exist(input_line, variable_memory, function_memory)
    if not input_line:
        return True
    # print("W/o vars:", input_line)

    # find all manually defined matrices, read them, and replace them with temporary variables
    while(input_line.find('[') != -1):
        open_index = input_line.find('[')
        close_index = input_line.find(']',open_index)+1
        np_matrix = np.array(read_matrix(input_line[open_index:close_index]))

        temp_name = ".matrix" + str(random.randrange(1000000))
        while temp_name in variable_memory.keys():
            temp_name = ".matrix" + str(random.randrange(1000000))

        variable_memory[temp_name] = np_matrix
        input_line = input_line[:open_index] + temp_name + input_line[close_index:]
        # print(variable_memory[temp_name])

    # iterate through the string and simplify it one step at a time following PEMDAS + replace computations as you go + error handle as you go
    while True:
        # 1). Find innermost set of parenthesis, evaluate, replace (__) with result, repeat
        while(input_line.find(')') != -1):
            first_close = input_line.find(')')
            first_open = input_line.rfind('(',0,first_close)
            inner_expression = input_line[first_open+1:first_close]  # +1 to exclude open para
            # evaluate the mini-expression
            valid_op, solution = evaluate(inner_expression,variable_memory)
            if valid_op == False: # break if error during evaluation
                return True
            # check if parenthesis correspond to function or not
            function_call, new_open = is_function(input_line, first_open, function_memory)
            if not function_call:
                # replace input_line w/ result
                input_line = input_line[:first_open] + str(solution) + input_line[first_close+1:]
            else:
                valid_op, solution = function_call(float(solution) if is_float(solution) else variable_memory[solution])
                if not valid_op: # break if error in function call
                    return True
                if not is_float(solution):
                    solution = create_temp_variable(solution,variable_memory)
                input_line = input_line[:new_open] + str(solution) + input_line[first_close+1:]
                
            # print(input_line)
        # store value + print if store_result == true else, just print
        valid_op, solution = evaluate(input_line,variable_memory)
        if valid_op == False: # break if error during evaluation
            return True
        
        solution = float(solution) if is_float(solution) else variable_memory[solution]
        if store_result:
            variable_memory[var_name] = solution
            print(var_name, '\n    ', variable_memory[var_name])
        else:
            print(solution)

        # remove temporary variables created during computation
        clean_memory(variable_memory)
        return True


def main():
    # create memory to store values
    variable_memory = dict()

    # Start read loop
    keep_looping = True
    while keep_looping:
        keep_looping = read_loop(variable_memory)

if __name__ == "__main__":
    main()