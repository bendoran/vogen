import re
from vogen.voparser import VoParser, VoVariable

class AS3VoParser( VoParser ):
    def parse( self, input_string, verbose ):
        self.input_string = input_string
        self.verbose = verbose
        
        class_names = re.findall(r"class (\w+)", self.input_string );
        
        #Find the class_name
        if len(class_names) > 0 :         
            if verbose :       
                print "Found Class"+class_names[0]
            class_name = class_names[0]
        else:
            print "Couldn't find class_name in Source File"
            return False
        
        #Find the properties
        variables = list()
        for variable in re.findall(r"private var ([\w\[\]]+) ?: ?(\w+)", self.input_string ):
            vo_variable = VoVariable( variable[0], variable[1] )
            variables.append( vo_variable )
            if self.verbose :
                print "Found Property: " + vo_variable.__str__()
                    
        if len( variables ) <= 0 :
            print "Couldn't find any variables in Source File, can't build a vo"
            return False
         
        return self.build_class( variables, class_name)
    
    def build_class(self, variables, class_name ):
        return_text = self.input_string
        
        #Rename all existing variables
        for variable in variables :
            return_text = return_text.replace( variable.variable_name, "_"+variable.variable_name )
        
        #Strip the last bracket
        return_text = return_text.rstrip('}')
        return_text = return_text.rstrip('}\n')
        
        #Print the Constructor
        return_text += "\n\t\tpublic function " + class_name + "( "
        for variable in variables :
            return_text += "\n\t\t\t" + variable.variable_name + " : " + variable.variable_type + " ,"
        return_text = return_text.rstrip(', ')
        return_text += "\n\t\t){"
        for variable in variables :
            return_text += "\n\t\t\tthis._" + variable.variable_name + " = " + variable.variable_name + ";"
        return_text += "\n\t\t}"
        
        #A bit of White Space
        return_text += "\n"
        
        #Print the Getters
        for variable in variables :
            return_text += "\n\t\tpublic function get " + variable.variable_name + "() : " + variable.variable_type + "{"
            return_text += "\n\t\t\treturn this._" + variable.variable_name + ";"
            return_text += "\n\t\t}"
            return_text += "\n"
            
        return_text += "\n\t}"
        return_text += "\n}"
        
        return return_text