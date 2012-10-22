class VoParser:
    def parse( self, inputString, verbose ):
        raise NotImplementedError
    
    def buildClass(self, variables, className ):
        raise NotImplementedError

class VoVariable:
    def __init__(self, variableName, variableType=None ):
        self.variableName = variableName;
        self.variableType = variableType;
        
    def __str__(self):
        return "Name: " + self.variableName + " Type: " + self.variableType
    