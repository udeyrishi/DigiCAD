#!/usr/bin/python3

"""
The main script running the CLI of the Digial Logic simplification tool: DigiCAD.
Needs python 3.4 to operate. Compatible mostly with any python 3.x, except for 
some quickly fixable syntactical issues (result of non-backwards syntax 
compatibility in successive python 3.x).

Tested for UNIX/Linux. Should work for most part on other OSes as well (except 
commands requiring bash). 

For help regarding the usage, see cli_help.txt, or launch command "help" from
the tool.

For best experience, make this and gui.py executable by "chmod a+x <filename>".
Then add it to your system path in ~/.bashrc.
"""

import cli_helper

# Defining the colours
green = cli_helper.bcolors.OKGREEN
head = cli_helper.bcolors.HEADER 
blue = cli_helper.bcolors.OKBLUE 
output = cli_helper.bcolors.WARNING
fail = cli_helper.bcolors.FAIL
endc = cli_helper.bcolors.ENDC

cli_helper.initialise() # Flash message

while(1):
    cli_helper.printc("\nDigiCAD: ", green, "") # Prompt
    user_ip_read = input()
    if user_ip_read.lower() == 'q' or user_ip_read.lower() == 'exit' \
        or user_ip_read.lower() == 'quit':
        # user asked to quit
        cli_helper.printc("Now quitting.\n", fail)
        break

    # First split is the command. Second, the arguments
    user_ip = user_ip_read.split(maxsplit = 1)
    if user_ip == []: continue # User pressed enter by mistake
    command = user_ip[0] # Parsing out the command

    if command in cli_helper.command_list:
        # Valid command
        arguments = user_ip[1] if (len(user_ip) > 1) else ""
        cli_helper.execute(command, arguments)

    elif command in cli_helper._workspace and len(user_ip) == 1:
        # User called a BF
        cli_helper.execute('display_BF', command) # Only the first argument will be taken 
    
    elif command in cli_helper._workspace and len(user_ip) > 1:
        # Possibility that some operator is acting on multiple BFs
        cli_helper.operator(user_ip_read)

    else:
        # Some syntax error
        cli_helper.printc("'%s' is neither a command, nor a BF in the workspace."\
                       %command, fail)