#!/usr/bin/env python
from vogen.as3parser import AS3VoParser
from vogen.javaparser import JavaVoParser
import argparse
import os.path
import re
import sys
                    
def run():

    #Get the input args
    argParser = argparse.ArgumentParser(description='VO Gen')
    argParser.add_argument('-i','--input', help='The source file to process',required=True)
    argParser.add_argument('-o','--output', help='The source file to save output to, if no output is provided output is printed to screen', required=False)
    argParser.add_argument('-s','--save', help='The output of the source file will be saved to the input file', action='store_true', required=False)
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
    
    if args['save'] :
        outputFilename = inputFilename 
    
    #Determine the Format
    fileName, fileExtension = os.path.splitext( inputFilename )
    
    if fileExtension == ".as" :
        voParser = AS3VoParser();
        if verbose : 
            print "Parsing AS3 Source File"
    elif fileExtension == ".java" :
        voParser = JavaVoParser();
        if verbose : 
            print "Parsing JAVA Source File"
    
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
                outputFile.write( outputText )
                outputFile.close()
            else:
                if verbose != True :
                    print outputText
    else:
        print "Input file format not recognised, supported formats (.as, .java)"







    