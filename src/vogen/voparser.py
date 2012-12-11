class VoParser:
    def parse( self, input_string, verbose ):
        raise NotImplementedError
    
    def build_class(self, variables, class_name ):
        raise NotImplementedError

class VoVariable:
    def __init__(self, variable_name, variable_type=None ):
        self.variable_name = variable_name;
        self.variable_type = variable_type;
        
    def __str__(self):
        return "Name: " + self.variable_name + " Type: " + self.variable_type
    