DigiCAD README
(Documentation and Instructions)

Developers: Udey Rishi and Raghav Vamaraju



OVERVIEW:
We have created a program that can evaluate, manipulate, and simplify Boolean 
functions. Given a Boolean function as an input (as a string), our program will
parse the string and create a Boolean Function object from it. This program uses
the self written module: boolfunc, consisting of the class BF and several 
functions. This module has a variety of methods and functions that can be used 
to analyze and/or simplify the function into different forms. For the algorithms 
used in various types of BF processing, see individual methods/functions in boolfunc.py.


*Our program is built in Python 3.3*. The command line is compatible with Python 3.4 as well. 
Our program may or may not be fully compatible with Python 3.2.



USAGE:
To run our program, you can use either the GUI or the command-line interface. *The GUI has some minor
glitches*, but is useful for quickly demostrating functionality. The command-line is more stable.
To test the functions individually, import boolfunc.py into a python3 command line (or iPython), and
all of the functions from all files will be imported. To create a Boolean function, you can use:
<variable_name> = BF("<function_definition>"),
and this will create an instance of the Boolean Function class. This class has many methods that can
manipulate the function. *The syntax for function definitions is outlined in the docstrings of strings.py*.



INSTALLATION:

GUI:
The GUI requires no installation. Simply run gui.py using python3 to open the GUI, and use either one
of the text boxes to input a function. The formatting/notation used in functions is described in detail 
in the docstrings of strings.py.

Command-Line:
The command line can also be run using python3, but it is recommended that the files cli.py and 
gui.py are made executable (using chmod a+x <filename>), and that the directory DigiCAD is added to the 
system path in ~/.bashrc. Not doing so may cause minor issues (inability to locate the help documentation 
and gui.py files). Functionality in the CLI will be the same either way.

The CLI requires interaction with the terminal (for colours), and system shell (for opening files and launching other
Python scripts). This is tested on Linux (so should work on any UNIX platform). It should work on any OS after adapting
the shell commands appropriately. It is compatible with the Ubuntu VMs that we use in CMPUT 275.



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
    documentation in cli_help.txt. Refer to cli_help.txt for help in using the command line, or use
    the 'help' command in the CLI itself.



SOURCES:
Quine-McCluskey Algorithm: http://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
GUI setup: http://www.tkdocs.com/tutorial/firstexample.html
Logo: Integrated graphic by <a href="http://www.freepik.com/">Freepik</a> from <a href="http://www.flaticon.com/">Flaticon</a> is licensed under <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0">CC BY 3.0</a>. Made with <a href="http://logomakr.com" title="Logo Maker">Logo Maker</a>
