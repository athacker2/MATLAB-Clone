import sys
import numpy as np
import re
import random

from input_handling import *
from expressions import *
from function_dict import function_memory

from Memory import Memory

def read_loop(variable_memory):
    """Function that interprets and evaluates each user line. It returns true to keep looping and false to exit"""
    # create regex for valid var names
    variable_format = re.compile(r'[^\W\d_]+[^\W]*')

    input_line = input(">> ")

    # exit loop
    if(input_line == "exit"):
        return False

    if(input_line == 'mem'):
        print(variable_memory)
        return True

    # identify if we are storing result or not
    store_result = True if input_line.find('=') != -1 else False

    # if we're storing the result, identify the variable name
    if store_result:
        var_name = input_line[:input_line.find('=')].strip()
        # if the variable name isn't valid throw error
        if(not variable_format.fullmatch(var_name)):
            print("Error: Invalid Variable Name '{var_name}'".format(var_name=var_name))
            return True
        # update the input line to only contain the expression to evaluate now
        input_line = input_line[input_line.find('=')+1:].strip()

    # ensure all variables used in expression are defined, else throw error, replace vars w/vals if all exist
    input_line = all_vars_exist(input_line, variable_memory, function_memory)
    if not input_line:
        return True

    # find all manually defined matrices, read them, and replace them with temporary variables
    while(input_line.find('[') != -1):
        open_index = input_line.find('[')
        close_index = input_line.find(']',open_index)+1
        np_matrix = read_matrix(input_line[open_index:close_index])

        temp_name = variable_memory.store_temp_matrix(np_matrix)
        input_line = input_line[:open_index] + temp_name + input_line[close_index:]

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
                valid_op, solution = function_call(float(solution) if is_float(solution) else variable_memory.get_value(solution))
                if not valid_op: # break if error in function call
                    return True
                if not is_float(solution):
                    solution = variable_memory.store_temp_matrix(solution)
                input_line = input_line[:new_open] + str(solution) + input_line[first_close+1:]
                
        # store value + print if store_result == true else, just print
        valid_op, solution = evaluate(input_line,variable_memory)
        if valid_op == False: # break if error during evaluation
            return True
        
        solution = float(solution) if is_float(solution) else variable_memory.get_value(solution)
        if store_result:
            variable_memory.add_value(var_name,solution)
            print(var_name, '\n    ', variable_memory.get_value(var_name))
        else:
            print(solution)

        # remove temporary variables created during computation
        variable_memory.clean()
        return True


def main():
    # create memory to store values
    variable_memory = Memory()

    # Start read loop
    keep_looping = True
    while keep_looping:
        keep_looping = read_loop(variable_memory)

if __name__ == "__main__":
    main()