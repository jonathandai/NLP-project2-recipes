class Directions(object):

    def __init__(self, directions, primary_cooking_method = None):
        self.directions = directions
        if primary_cooking_method == None:
            self.primary_cooking_method = self.get_primary_cooking_method(directions)
        else:
            self.primary_cooking_method = primary_cooking_method
        
    def get_primary_cooking_method(self, directions):
        # extra primary cooking method from insutrctions
        return ""

    def to_healthy(self):
        # convert ingredient to healthy substitute
        pass

    

    