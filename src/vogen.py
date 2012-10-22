#!/usr/bin/env python
import argparse
import os.path
import re
import sys

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
        for variable in re.findall(r"private var ([\w\[\]]+) : (\w+)", self.inputString ):
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
        returnText += "\n\t\tpublic " + className + "( "
        for variable in variables :
            returnText += "\n\t\t\t" + variable.variableName + " : " + variable.variableType + " ,"
        returnText = returnText.rstrip(', ')
        returnText += "\n\t\t){"
        for variable in variables :
            returnText += "\n\t\t\t this._" + variable.variableName + " = " + variable.variableName + ";"
        returnText += "\n\t\t}"
        
        #A bit of White Space
        returnText += "\n"
        
        #Print the Getters
        for variable in variables :
            returnText += "\n\t\t public function set " + variable.variableName + "() : " + variable.variableType + "{"
            returnText += "\n\t\t\t return this._" + variable.variableName + ";"
            returnText += "\n\t\t }"
            returnText += "\n"
        
        return returnText
                    
'''class JavaVoParser( VoParser ):
    def parse( self, inputString, verbose ):
        classNames = re.findall(r"class (\w+)", text );
          
        #Find the ClassName
        if len(classNames) > 0 :         
            if verbose :       
                print "Found "+classNames[0]
            className = classNames[0]
        else:
            print "Couldn't find ClassName in Source File: " + args['input']
            return False

        #Find the properties
        variables = re.findall(r"private ([\w\[\]]+) (\w+)", text )
        if len( variables ) > 0 :
            if verbose :
                for variable in variables : 
                    print "Found Property: " + variable[1] + " of Type: " + variable[0]
        else:
            print "Couldn't find any variables in Source File, can't build a vo"
            return False
            
        #Generate the new source code
        #Strip last bracket
        text = text.rstrip('}')
        text = text.rstrip('}\n')
        
        #build the constructor
        text = text + "\n\tpublic " + className + "( "
        for variable in variables :  
            text = text + variables[0] + " " + variables[1] + ", "
        text = text.rstrip(', ')
        text = text +" ){\n"
        for variable in variables :  
            text = text + "\t\tthis." + variable[1] + " = " + variable[1] + ";\n"
        text = text + "\t}\n"
        
        #Build the Getters
        for variable in variables :  
            text = text + "\n\tpublic " + variable[0] + " get" + variable[1].title() + "(){\n\t\treturn " +  variable[1] + ";\n\t}\n"
        
        #Put the last brace back on
        text = text + "}"
        
        return text
'''
            
if __name__ == "__main__":

    #Get the input args
    argParser = argparse.ArgumentParser(description='VO Gen')
    argParser.add_argument('-i','--input', help='The source file to process',required=True)
    argParser.add_argument('-o','--output', help='The source file to save output to, if no output is provided output is saved to the input file', required=False)
    argParser.add_argument('-v','--verbose', help='Enables verbose messaging', action='store_true', required=False)
    args = vars( argParser.parse_args() )
    
    #Input Filename is Required
    inputFilename = args['input'];
    
    outputFilename = None
    verbose = False
    
    #Get the OutPut Filename if it's set
    if args['output'] :
        outputFilename = args['output']
        
    if args['verbose'] :
        verbose = True;
    
    #Determine the Format
    fileName, fileExtension = os.path.splitext( inputFilename )
    
    if fileExtension == ".as" :
        voParser = AS3VoParser();
        if verbose : 
            print "Parsing AS3 Source File"
    '''
    elif fileExtension == ".java" :
        voParser = JavaVoParser();
        if verbose : 
            print "Parsing JAVA Source File"
    '''
            
    
    if voParser:
        
        #Open the File
        inputFile = open( inputFilename )
        inputText = inputFile.read()
        inputFile.close()
        
        #Parse the input
        outputText = voParser.parse( inputText, verbose )
        
        if outputText :
            #Output the result
            if verbose : 
                print "\n\n=======================\n=Resulting Source Code=\n=======================\n\n" + outputText
                        
            if outputFilename != None : 
                outputFile = open( outputFilename, 'w+')
            else:
                outputFile = open( inputFilename, 'w+')
                    
                #Close the output file
                outputFile.write( outputText )
                outputFile.close()
    else:
        print "Input file format not recognised, supported formats (.as, .java)"
    
    sys.exit();








    