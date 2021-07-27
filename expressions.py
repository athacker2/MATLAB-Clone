import re

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
# 2). Variable support is a thing, but still a little finicky at times (i.e. if input is only a var)
# 3). Maybe replace all variables w/their values immediately instead of one at a time? (during error handling step??)
def evaluate(expression, variable_memory):
    """Takes input for an expression w/o grouping symbols and evaluates it following PEMDAS (minus the P)"""
    expression = expression.replace(' ','') # removes all spaces (might cause issues w/matrices later on)
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
        # evaluate
        if op_pos == mul_pos:
            solution = float(left_operand)*float(right_operand)
        else:
            solution = float(left_operand)/float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
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
        # evaluate
        if op_pos == add_pos:
            solution = float(left_operand)+float(right_operand)
        else:
            solution = float(left_operand)-float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        #print(expression)
    #print("Final Expression:", expression)
    return expression