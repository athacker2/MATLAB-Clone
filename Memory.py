class Memory:
    variable_memory = dict()

    def clean_memory(self):
        """Clears all temporary matrices from memory created during computation of expression"""
        delete = [key for key in self.variable_memory if key[0:7] == ".matrix"]
        for key in delete: del self.variable_memory[key]