from vogen.parser import VoParser, VoVariable
import re

class PHPParser( VoParser ):
    
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
        for variable in re.findall(r"private \$(\w+)", self.inputString ):
            voVariable = VoVariable( variable, "" )
            variables.append( voVariable )
            if self.verbose :
                print "Found Property: " + voVariable.__str__()
            
        if len( variables ) <= 0 :
            print "Couldn't find any variables in Source File, can't build a vo"
            return False
        
        return self.buildClass( variables, className)
    
     def buildClass(self, variables, className ):
        #Generate the new source code
        returnText = self.inputString
        
        #Strip the last bracket
        returnText = returnText.rstrip('}')
        returnText = returnText.rstrip('}\n')
        
        #build the constructor
        returnText = returnText + "\n\tpublic " + className + "( "
        for variable in variables :  
            returnText = returnText + "$" + variable.variableName + ","
        returnText = returnText.rstrip(', ')
        returnText = returnText +" ){\n"
        for variable in variables :  
            returnText = returnText + "\t\tthis->" + variable.variableName + " = $" + variable.variableName + ";\n"
        returnText = returnText + "\t}\n"
        
        #Build the Getters
        for variable in variables :  
            returnText = returnText + "\n\tpublic get" + variable.variableName[0].upper() + variable.variableName[1:] + "(){\n\t\treturn $this->" +  variable.variableName + ";\n\t}\n"
        
        #Put the last brace back on
        returnText = returnText + "}"
        
        return returnText
