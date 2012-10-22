#VO Generator

This is a utility for generating [Value Objects](http://en.wikipedia.org/wiki/Value_object) used in model to class mappings in various frameworks and technologies.

Value Objects often take lots of boring copy & pasting to generate and constant typing has led me to make this pretty quickly build utility, the tool allows you to write just the variables with types for your value objects. Using the tool the constructor and get functions are auto generated.

The resulting output can either be saved to a new file, printed to screen, or overwrite the existing source.

## Language Support

So far vogen can generate Value Objects for the following languages

* Actionscript 3
* Java

## Usage

`vogen -i INPUT [-o OUTPUT] [-s] [-v]`

### Syntax

<u>Required</u>

**-i --input INPUT_FILENAME**: The File name of VO to process

<u>Optional</u>

**-o --output OUTPUT_FILENAME** The File name of VO to output too, will create the file if it doesn't exist
	
**-s --save** Optional parameter to save the output directly to the input file, effectively overwriting it

**-v --verbose** Vebose mode, will print out all the stages of the process

### Examples

*These examples are executed from the bin directory of the project*

* Print to Screen: `./vogen -i ../tests/as3vo.as`
* Output to New File: `./vogen -i ../tests/as3vo.as -o ../tests/as3vonew.as`
* Save to Original File: `./vogen -i ../tests/as3vo.as -s`
* Print to Screen (Verbose): `./vogen -i ../tests/as3vo.as -v`

