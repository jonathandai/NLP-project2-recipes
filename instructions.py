class Instructions(object):

    def __init__(self, instructions, primary_cooking_method = None):
        self.instructions = instructions
        if primary_cooking_method == None:
            self.primary_cooking_method = self.get_primary_cooking_method(instructions)
        else:
            self.primary_cooking_method = primary_cooking_method
        
    def get_primary_cooking_method(self, instructions):
        # extra primary cooking method from insutrctions
        return ""

    def to_healthy(self):
        # convert ingredient to healthy substitute
        pass

    

    