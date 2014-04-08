#!/usr/bin/python3

"""
The main script running the custom made interpreted CAD tool language: DigiCAD.
Needs python3 to operate.
"""

import cli_data

# Defining the colours
green = cli_data.bcolors.OKGREEN
head = cli_data.bcolors.HEADER 
blue = cli_data.bcolors.OKBLUE 
output = cli_data.bcolors.WARNING
fail = cli_data.bcolors.FAIL
endc = cli_data.bcolors.ENDC

cli_data.initialise()

while(1):
    cli_data.printc("\nDigiCAD: ", green, "")
    user_ip_read = input()
    if user_ip_read.lower() == 'q' or user_ip_read.lower() == 'exit' \
        or user_ip_read.lower() == 'quit':
        # user asked to quit
        cli_data.printc("Now quitting.\n", fail)
        break

    # First split is the command
    user_ip = user_ip_read.split(maxsplit = 1)
    if user_ip == []: continue # User pressed enter by mistake
    command = user_ip[0] # Parsing out the command

    if command in cli_data.command_list:
        arguments = user_ip[1] if (len(user_ip) > 1) else ""
        cli_data.execute(command, arguments)

    elif command in cli_data._workspace and len(user_ip) == 1:
        # User called a BF
        cli_data.execute('display_BF', command) # Only the first argument will be taken 
    
    elif command in cli_data._workspace and len(user_ip) > 1:
        # Possibility that some operator is acting on multiple BFs
        cli_data.operator(user_ip_read)

    else:
        cli_data.printc("'%s' is neither a command, nor a BF in the workspace." %command,\
               fail)


