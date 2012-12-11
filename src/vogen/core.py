#!/usr/bin/env python
import argparse
from vogen.as3parser import AS3VoParser
import sys
from vogen.javaparser import JavaVoParser
from vogen.phpparser import PHPParser
#from vogen.javaparser import JavaVoParser
#from vogen.phpparser import PHPParser
                    
def run():
    #Get the input args
    argParser = argparse.ArgumentParser(description='VO Gen')
    argParser.add_argument('-i','--input', help='The source file to process',required=False)
    argParser.add_argument('-o','--output', help='The source file to save output to, if no output is provided output is printed to screen', required=False)
    argParser.add_argument('-s','--save', help='The output of the source file will be saved to the input file', action='store_true', required=False)
    argParser.add_argument('-v','--verbose', help='Enables verbose messaging', action='store_true', required=False)
    args = vars( argParser.parse_args() )
    
    #Input Filename is Required
    input_filename = args['input'];
    
    output_filename = None
    verbose = False
    
    #Get the OutPut Filename if it's set
    if args['output'] :
        output_filename = args['output']
    if args['verbose'] :
        verbose = True;
    if args['save'] :
        output_filename = input_filename 
    
    vo_parser = None
    
    #Assertain Which VO Parser We Want to Use
    if ".as" in input_filename :
        vo_parser = AS3VoParser();
        if verbose : 
            print "Parsing AS3 Source File"
    elif ".java" in input_filename :
        vo_parser = JavaVoParser();
        if verbose : 
            print "Parsing JAVA Source File"
    elif ".php" in input_filename :
        vo_parser = PHPParser();
        if verbose : 
            print "Parsing PHP Source File"
            
    if vo_parser:
        
        #Open the File
        input_file = open( input_filename )
        input_text = input_file.read()
        input_file.close()
        
        #Parse the input
        output_text = vo_parser.parse( input_text, verbose )
        
        if output_text :
            #Output the result
            if verbose : 
                print "\n\n=======================\n=Resulting Source Code=\n=======================\n\n" + output_text
                        
            if output_filename != None : 
                output_file = open( output_filename, 'w+')
                output_file.write( output_text )
                output_file.close()
            else:
                if verbose != True :
                    print output_text
    else:
        print "Input file format not recognised, supported formats (.as, .java, .php)"







    