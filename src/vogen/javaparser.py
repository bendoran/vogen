from vogen.voparser import VoParser, VoVariable

import re
class JavaVoParser( VoParser ):
    def parse( self, input_string, verbose ):
        
        self.input_string = input_string
        self.verbose = verbose
        
        class_names = re.findall(r"class (\w+)", self.input_string )
          
        #Find the class_name
        if len(class_names) > 0 :         
            if verbose :       
                print "Found "+class_names[0]
            class_name = class_names[0]
        else:
            print "Couldn't find class_name in Source File"
            return False

        #Find the properties
        variables = list()
        for variable in re.findall(r"private ([\w\[\]]+) (\w+)", self.input_string ):
            vo_variable = VoVariable( variable[1], variable[0] )
            variables.append( vo_variable )
            if self.verbose :
                print "Found Property: " + vo_variable.__str__()
            
        if len( variables ) <= 0 :
            print "Couldn't find any variables in Source File, can't build a vo"
            return False
        
        return self.build_class( variables, class_name)
        
    def build_class(self, variables, class_name ):
        #Generate the new source code
        return_text = self.input_string
        
        #Strip the last bracket
        return_text = return_text.rstrip('}')
        return_text = return_text.rstrip('}\n')
        
        #build the constructor
        return_text = return_text + "\n\tpublic " + class_name + "( "
        for variable in variables :  
            return_text = return_text + variable.variable_name + " " + variable.variable_type + ", "
        return_text = return_text.rstrip(', ')
        return_text = return_text +" ){\n"
        for variable in variables :  
            return_text = return_text + "\t\tthis." + variable.variable_name + " = " + variable.variable_name + ";\n"
        return_text = return_text + "\t}\n"
        
        #Build the Getters
        for variable in variables :  
            return_text = return_text + "\n\tpublic " + variable.variable_type + " get" + variable.variable_name[0].upper() + variable.variable_name[1:] + "(){\n\t\treturn " +  variable.variable_name + ";\n\t}\n"
        
        #Put the last brace back on
        return_text = return_text + "}"
        
        return return_text