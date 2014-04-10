DigiCAD README
(Documentation and Instructions)

Developers: Udey Rishi and Raghav Vamaraju



OVERVIEW:
We have created a program that can evaluate, manipulate, and simplify Boolean functions.
Given a Boolean function as an input (as a string), our program will parse the string and
create a Boolean Function object from it. This object has a variety of methods that can be used
to analyze and/or simplify the function into different forms. The simplification is done using
the Quine-McCluskey algorithm.



USAGE:
To run our program, you can use either the GUI or the command-line interface. *The GUI has several
glitches*, but is useful for quickly demostrating functionality. The command-line is more stable.
To test the functions individually, import boolfunc.py into a python3 command line (or iPython), and
all of the functions from all files will be imported. To create a Boolean function, you can use:
<variable_name> = BF("<function_definition>"),
and this will create an instance of the Boolean Function class. This class has many methods that can
manipulate the function. *The syntax for function definitions is outlined in the docstrings of strings.py*.



INSTALLATION:

GUI:
1. The GUI requires no installation. Simply run gui.py using python3 to open the GUI, and use either one
   of the text boxes to input a function. The formatting/notation used in functions is described in detail 
   in the docstrings of strings.py.

Command-Line:
1. <UDEY, WRITE THE INSTALLATION INSTRUCTIONS FOR THE COMMAND LINE HERE>



DETAILS ABOUT THE CODE:

In strings.py:
--> parse() is used to parse a string of a Boolean function.

In truth_tables.py:
--> make_table() is used to create a truth table (after parsing the string).

In boolfunc.py:
--> the BF() class takes in a function definition (a string) as an argument.

In gui.py:
--> The GUI is built from Tkinter. Tkinter comes with Python 3 and does not require external installation.

In cli.py:
--> The command line uses cli_helper.py for the majority of its functionality. It has extensive help 
    documentation in cli_help.txt. Refer to cli_help.txt for help in using the command line.



SOURCES:
Quine-McCluskey Algorithm: http://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
GUI setup: http://www.tkdocs.com/tutorial/firstexample.html