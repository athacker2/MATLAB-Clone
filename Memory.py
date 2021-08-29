import random

class Memory:
    variable_memory = dict()

    def add_value(self, key, value):
        self.variable_memory[key] = value
    
    def get_value(self,key):
        assert Memory.contains_var(self,key)
        return self.variable_memory[key]
    
    def contains_var(self,key):
        if key in self.variable_memory.keys():
            return True
        else:
            return False
    
    def store_temp_matrix(self,matrix):
        """Generates a random variable name, stores the input matrix into a dict under that name, and returns the variable name"""
        var_name = ".matrix" + str(random.randrange(1000000)) # probs replace this magic number later : P
        while var_name in self.variable_memory.keys():
            var_name = ".matrix" + str(random.randrange(1000000))
        self.variable_memory[var_name] = matrix
        return var_name

    def clean(self):
        """Clears all temporary matrices from memory created during computation of expression"""
        delete = [key for key in self.variable_memory if key[0:7] == ".matrix"]
        for key in delete: del self.variable_memory[key]
    
    def __repr__(self):
        print("Memory: ", [(key,self.variable_memory[key]) for key in self.variable_memory.keys])