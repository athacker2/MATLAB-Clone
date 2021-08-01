from input_handling import is_float
import re
import numpy as np
import random

char_reqs = re.compile(r'[\w.]')
num_reqs = re.compile(r'(-{,1}\d+(?:\.\d+)?)')

def find_operation_bounds(expression, op_index):
    # find left operand
    j = op_index-1
    while j > 0 and char_reqs.fullmatch(expression[j]):
        j = j - 1
    left_limit = 0 if j == 0 else j+1
    if left_limit != 0 and expression[left_limit-1] == '-': # allow negatives
        left_limit = left_limit-1
    # find right operand
    j = op_index+1
    if expression[j] == '-': # allow negatives
        j = j + 1
    while j < len(expression) and char_reqs.fullmatch(expression[j]) :
        j = j + 1

    right_limit = j+1 if j == len(expression) else j
    return left_limit,right_limit

# To Do:
# 1). Add Matrix Support
def evaluate(expression, variable_memory):
    """Takes input for an expression w/o grouping symbols and evaluates it following PEMDAS (minus the P)"""
    expression = expression.replace(' ','') # removes all spaces (might cause issues w/matrices later on)
    expression = expression.replace('--','+') # remove double negative (this is the ONLY dup negative handling i'm going to do)
    while(expression.find('^') != -1): # start with exponentials
        exponent_pos = expression.find('^')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression, exponent_pos)
        base_var = expression[left_limit:exponent_pos].strip()
        exponent_var = expression[exponent_pos+1:right_limit].strip()
        # evaluate 
        solution = pow(float(base_var),float(exponent_var))
        # check for 'negative gobble'
        if solution > 0 and base_var[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        #print(expression)
    while(expression.find('*') != -1 or expression.find('/') != -1): # do mul/div next
        mul_pos = expression.find('*')
        div_pos = expression.find('/')
        op_pos = div_pos if (div_pos < mul_pos and div_pos != -1 or mul_pos == -1) else mul_pos
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,op_pos)
        left_operand = expression[left_limit:op_pos].strip()
        right_operand = expression[op_pos+1:right_limit].strip()
        # cast operand to appropriate type
        left_operand = float(left_operand) if is_float(left_operand) else variable_memory[left_operand]
        right_operand = float(right_operand) if is_float(right_operand) else variable_memory[right_operand]
        # evaluate
        if op_pos == mul_pos:
            if not is_float(left_operand) and not is_float(right_operand):
                if left_operand.shape[1] == right_operand.shape[0]:
                    solution = left_operand @ right_operand
                else:
                    print("Error: Mismatch in array dimensions")
                    return False
            solution = float(left_operand)*float(right_operand)
        else:
            solution = float(left_operand)/float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and str(left_operand)[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        #print(expression)
    while(expression.find('+',1) != -1 or expression.find('-',1) != -1): # do add/sub next (start search from 1 past to ignore leading + and - signs)
        add_pos = expression.find('+',1)
        sub_pos = expression.find('-',1)
        op_pos = sub_pos if (sub_pos < add_pos and sub_pos != -1 or add_pos == -1) else add_pos
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,op_pos)
        left_operand = expression[left_limit:op_pos].strip()
        right_operand = expression[op_pos+1:right_limit].strip()
        # cast operand to appropriate type
        left_operand = float(left_operand) if is_float(left_operand) else variable_memory[left_operand]
        right_operand = float(right_operand) if is_float(right_operand) else variable_memory[right_operand]
        # evaluate
        if op_pos == add_pos:
            solution = left_operand+right_operand
        else:
            solution = left_operand-right_operand
        # create temporary matrix if needed
        if not is_float(solution):
            solution = create_temp_variable(solution, variable_memory)
        # check for 'negative gobble'
        if str(left_operand)[0] == '-':
            if is_float(solution) and solution > 0:
                solution = '+' + str(solution)
            elif not is_float(solution):
                solution = '+' + str(solution)
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        #print(expression)
    #print("Final Expression:", expression)
    return float(expression) if is_float(expression) else variable_memory[expression]

def create_temp_variable(matrix, variable_memory):
    """Generates a random variable name, stores the input matrix into a dict under that name, and returns the variable name"""
    var_name = ".matrix" + str(random.randrange(1000000)) # probs replace this magic number later : P
    while var_name in variable_memory.keys():
        var_name = ".matrix" + str(random.randrange(1000000))
    variable_memory[var_name] = matrix
    return var_name