
class ingredient(object):

    def __init__(self, name, quanitity, unit):
        # TODO: Deal with parsing for standarized units
        self.name = name
        self.quanitity = quanitity
        self.unit = unit

    def to_healthy(self):
        # convert ingredient to healthy substitute
        pass
    
    def to_veg(self):
        # convert ingredient to veg substitutde
        pass
    

