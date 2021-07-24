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
        # evalate exponential
        if not num_reqs.fullmatch(base_var):
            lookup = variable_memory[base_var.replace('-','')]
            base_var = lookup if base_var[0] != '-' else -1*lookup
        if not num_reqs.fullmatch(exponent_var):
            lookup = variable_memory[exponent_var.replace('-','')]
            exponent_var = lookup if exponent_var[0] != '-' else -1*lookup
        solution = pow(float(base_var),float(exponent_var))
        # check for 'negative gobble'
        if solution > 0 and base_var[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        # print(expression)
    while(expression.find('*') != -1): # do multiplication next
        mul_pos = expression.find('*')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,mul_pos)
        left_operand = expression[left_limit:mul_pos].strip()
        right_operand = expression[mul_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            lookup = variable_memory[left_operand.replace('-','')]
            left_operand = lookup if left_operand[0] != '-' else -1*lookup
        if not num_reqs.fullmatch(right_operand):
            lookup = variable_memory[right_operand.replace('-','')]
            right_operand = lookup if right_operand[0] != '-' else -1*lookup
        solution = float(left_operand)*float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        # print(expression)
    while(expression.find('/') != -1): # do division next
        div_pos = expression.find('/')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,div_pos)
        left_operand = expression[left_limit:div_pos].strip()
        right_operand = expression[div_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            lookup = variable_memory[left_operand.replace('-','')]
            left_operand = lookup if left_operand[0] != '-' else -1*lookup
        if not num_reqs.fullmatch(right_operand):
            lookup = variable_memory[right_operand.replace('-','')]
            right_operand = lookup if right_operand[0] != '-' else -1*lookup
        solution = float(left_operand)/float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        # print(expression)
    while(expression.find('+') != -1): # do addition next
        add_pos = expression.find('+')
        #find operands
        left_limit,right_limit = find_operation_bounds(expression,add_pos)
        left_operand = expression[left_limit:add_pos].strip()
        right_operand = expression[add_pos+1:right_limit].strip()
        # evalate
        if not num_reqs.fullmatch(left_operand):
            lookup = variable_memory[left_operand.replace('-','')]
            left_operand = lookup if left_operand[0] != '-' else -1*lookup
        if not num_reqs.fullmatch(right_operand):
            lookup = variable_memory[right_operand.replace('-','')]
            right_operand = lookup if right_operand[0] != '-' else -1*lookup
        solution = float(left_operand)+float(right_operand)
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        # print(expression)
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
        # check for 'negative gobble'
        if solution > 0 and left_operand[0] == '-':
            solution = '+' + str(solution)
        # update expression
        expression = expression[:left_limit] + str(solution) + expression[right_limit:]
        # print(expression)
    # print("Final Expression:", expression)
    return expression