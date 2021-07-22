import sys
import numpy as np
import re

from advanced_ops import *
from input_handling import *

char_reqs = re.compile(r'[\w.]')
num_reqs = re.compile(r'(\d+(?:\.\d+)?)')

def find_operation_bounds(expression, op_index):
    # find left operand
    j = op_index-1
    while expression[j] == ' ': # skip spaces
        j = j -1
    while j > 0 and char_reqs.fullmatch(expression[j]):
        j = j - 1
    left_limit = 0 if j == 0 else j+1
    # find right operand
    j = op_index+1
    while expression[j] == ' ': # skip spaces
        j = j + 1
    while j < len(expression) and char_reqs.fullmatch(expression[j]) :
        j = j + 1
    right_limit = j+1 if j == len(expression) else j
    return left_limit,right_limit

# does NOT have matrix support yet. Also not much error handling
def evaluate(expression, variable_memory):
    """Takes input for an expression w/o grouping symbols and evaluates it following PEMDAS (minus the P)"""
    while(expression.find('^') != -1): # start with exponentials
        exponent_pos = expression.find('^')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression, exponent_pos)
        base_var = expression[left_limit:exponent_pos].strip()
        exponent_var = expression[exponent_pos+1:right_limit].strip()
        # evalate exponential
        if not num_reqs.fullmatch(base_var):
            base_var = variable_memory[base_var]
        if not num_reqs.fullmatch(exponent_var):
            exponent_var = variable_memory[exponent_var]
        solution = pow(float(base_var),float(exponent_var))
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        print(expression)
    while(expression.find('*') != -1): # do multiplication next
        mul_pos = expression.find('*')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,mul_pos)
        left_operand = expression[left_limit:mul_pos].strip()
        right_operand = expression[mul_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            left_operand = variable_memory[left_operand]
        if not num_reqs.fullmatch(right_operand):
            right_operand = variable_memory[right_operand]
        solution = float(left_operand)*float(right_operand)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        print(expression)
    while(expression.find('/') != -1): # do division next
        div_pos = expression.find('/')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,div_pos)
        left_operand = expression[left_limit:div_pos].strip()
        right_operand = expression[div_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            left_operand = variable_memory[left_operand]
        if not num_reqs.fullmatch(right_operand):
            right_operand = variable_memory[right_operand]
        solution = float(left_operand)/float(right_operand)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        print(expression)
    while(expression.find('+') != -1): # do addition next
        add_pos = expression.find('+')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,add_pos)
        left_operand = expression[left_limit:add_pos].strip()
        right_operand = expression[add_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            left_operand = variable_memory[left_operand]
        if not num_reqs.fullmatch(right_operand):
            right_operand = variable_memory[right_operand]
        solution = float(left_operand)+float(right_operand)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        print(expression)
    while(expression.find('-') != -1): # do subtraction next
        sub_pos = expression.find('-')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,sub_pos)
        left_operand = expression[left_limit:sub_pos].strip()
        right_operand = expression[sub_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            left_operand = variable_memory[left_operand]
        if not num_reqs.fullmatch(right_operand):
            right_operand = variable_memory[right_operand]
        solution = float(left_operand)-float(right_operand)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        print(expression)
    print("Final Expression:", expression)
    return expression



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
            print("Expression:", input_line)

        # ensure all variables used in expression are defined, else throw error
        if not all_vars_exist(input_line, variable_memory):
            continue

        # iterate through the string and simplify it one step at a time following PEMDAS + replace computations as you go + error handle as you go
        while True:
            # 1). Find innermost set of parenthesis, evaluate, replace (__) with result, repeat
            while(input_line.find(')') != -1):
                first_close = input_line.find(')')
                first_open = input_line.rfind('(',0,first_close)
                inner_expression = input_line[first_open+1:first_close]
                print(inner_expression) # +1 to exclude open para
                # evaluate(inner_expression) <-- function should basically systematically apply EMDAS
                solution = evaluate(inner_expression,variable_memory)
                # replace input_line[first_open:first_close+1] w/ result
                input_line = input_line[:first_open] + str(solution) + input_line[first_close+1:]
                print(input_line)
            # ideally once grouping symbols gone, just call evaluate(input_line) once to solve rest of expression
            # store value + print if store_result == true else, just print
            print("Input w/o paras:", input_line)
            print(evaluate(input_line,variable_memory))
            break


            


# Major Cases:
# Assignment vs no-assigment
# Computation regardless of above case using order of ops.
#   1). Grouping
#   2). Mul/Div
#   3). Add/Sub

if __name__ == "__main__":
    main()