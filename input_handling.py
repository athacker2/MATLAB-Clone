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
            # print("Variable:", variable)
            if(not (variable in variable_memory.keys())):
                print("Error: Variable {variable} is not in memory.".format(variable=variable))
                return False
    return True

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