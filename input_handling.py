import re

def all_vars_exist(input_line, variable_memory):
    char_reqs = re.compile(r'[^\W]')
    j = -1
    for i, char in enumerate(input_line):
        if i<j:
            continue
        if char.isalpha(): # found a variable
            j = i
            while(j < len(input_line) and char_reqs.fullmatch(input_line[j])):
                j = j + 1
            variable = input_line[i:j]
            print("Variable:", variable)
            if(not (variable in variable_memory.keys())):
                print("Error: Variable {variable} is not in memory.".format(variable=variable))
                return False
    return True