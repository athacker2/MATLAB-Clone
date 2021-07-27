import sys
import numpy as np
import re

from advanced_ops import *
from input_handling import *
from expressions import *

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

        if(input_line == 'mem'):
            print(variable_memory)
            continue

        # identify if we are storing result or not
        store_result = True if input_line.find('=') != -1 else False

        # if we're storing the result, identify the variable name
        if store_result:
            var_name = input_line[:input_line.find('=')].strip()
            # print(var_name)
            # if the variable name isn't valid throw error
            if(not variable_format.fullmatch(var_name)):
                print("Invalid Variable Name : {var_name}".format(var_name=var_name))
                continue
            # update the input line to only contain the expression to evaluate now
            input_line = input_line[input_line.find('=')+1:].strip()
            # print("Expression:", input_line)

        # ensure all variables used in expression are defined, else throw error, replace vars w/vals if all exist
        input_line = all_vars_exist(input_line, variable_memory)
        if not input_line:
            continue
        print("W/o vars:", input_line)

        # iterate through the string and simplify it one step at a time following PEMDAS + replace computations as you go + error handle as you go
        while True:
            # 1). Find innermost set of parenthesis, evaluate, replace (__) with result, repeat
            while(input_line.find(')') != -1):
                first_close = input_line.find(')')
                first_open = input_line.rfind('(',0,first_close)
                inner_expression = input_line[first_open+1:first_close]  # +1 to exclude open para
                # print(inner_expression)
                # evaluate the mini-expression
                solution = evaluate(inner_expression,variable_memory)
                # replace input_line w/ result
                input_line = input_line[:first_open] + str(solution) + input_line[first_close+1:]
                # print(input_line)
            # store value + print if store_result == true else, just print
            solution = evaluate(input_line,variable_memory)
            if store_result:
                variable_memory[var_name] = solution
                print(var_name, '\n    ', variable_memory[var_name])
            else:
                print(solution)
            break


            


# Major Cases:
# Assignment vs no-assigment
# Computation regardless of above case using order of ops.
#   1). Grouping
#   2). Mul/Div
#   3). Add/Sub

if __name__ == "__main__":
    main()