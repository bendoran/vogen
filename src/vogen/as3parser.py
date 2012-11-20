from vogen.parser import VoParser, VoVariable
import re

class AS3VoParser( VoParser ):
    def parse( self, inputString, verbose ):
        self.inputString = inputString
        self.verbose = verbose
        
        classNames = re.findall(r"class (\w+)", self.inputString );
        
        #Find the ClassName
        if len(classNames) > 0 :         
            if verbose :       
                print "Found Class"+classNames[0]
            className = classNames[0]
        else:
            print "Couldn't find ClassName in Source File"
            return False
        
        #Find the properties
        variables = list()
        for variable in re.findall(r"private var ([\w\[\]]+)( )?:( )?(\w+)", self.inputString ):
            voVariable = VoVariable( variable[0], variable[1] )
            variables.append( voVariable )
            if self.verbose :
                print "Found Property: " + voVariable.__str__()
                    
        if len( variables ) <= 0 :
            print "Couldn't find any variables in Source File, can't build a vo"
            return False
         
        return self.buildClass( variables, className)
    
    def buildClass(self, variables, className ):
        returnText = self.inputString
        
        #Rename all existing variables
        for variable in variables :
            returnText = returnText.replace( variable.variableName, "_"+variable.variableName )
        
        #Strip the last bracket
        returnText = returnText.rstrip('}')
        returnText = returnText.rstrip('}\n')
        
        #Print the Constructor
        returnText += "\n\t\tpublic function " + className + "( "
        for variable in variables :
            returnText += "\n\t\t\t" + variable.variableName + " : " + variable.variableType + " ,"
        returnText = returnText.rstrip(', ')
        returnText += "\n\t\t){"
        for variable in variables :
            returnText += "\n\t\t\tthis._" + variable.variableName + " = " + variable.variableName + ";"
        returnText += "\n\t\t}"
        
        #A bit of White Space
        returnText += "\n"
        
        #Print the Getters
        for variable in variables :
            returnText += "\n\t\tpublic function get " + variable.variableName + "() : " + variable.variableType + "{"
            returnText += "\n\t\t\treturn this._" + variable.variableName + ";"
            returnText += "\n\t\t}"
            returnText += "\n"
            
        returnText += "\n\t}"
        returnText += "\n}"
        
        return returnText