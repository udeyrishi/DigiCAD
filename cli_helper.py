"""
This is the helper file for cli.py. See cli.py or Readme.txt for details.
Developed by: Udey Rishi, 2014
"""

from boolfunc import *
import sys, copy, os

class bcolors:
    """
    The class for generating colour text in the Linux terminal. 

    Source:
    http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-
    using-python
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# For ease of reference
green = bcolors.OKGREEN
head = bcolors.HEADER 
blue = bcolors.OKBLUE 
output = bcolors.WARNING
fail = bcolors.FAIL
endc = bcolors.ENDC

# Stores all the created boolean functions mapped to their function name.
_workspace = {}

# Internal functions
def printc(text, colour = output, term = "\n"):
    """
    Prints the given text in colour. See class bcolors for list of allowed
    colours.
    """
    print((colour + "%s" + bcolors.ENDC) %text , end = term)

def find_name_hard(function):
    """
    Looks for a name in the partial proper BF format: f = <expression>.
    Adds to the functionality of "find_name" in strings.py.
    """
    rv = ""
    for i in range(len(function)):
        if function[i] != "=": 
            rv += function[i]
        elif i+1 < len(function) and function[i+1] != "=":
            return rv.strip()

def execute(command, args):
    """
    Executes the command mentioned. Passes the args as the argument
    to the command. The command must be in command_list, and the # of args in 
    the space seperated argument list should be in the arg_len. 
    """
    func = command_list[command] 

    if len(args.split()) not in arg_len[command] and \
        command not in ["def", "equal", "or", "and", "xor", "nor", "nand"]:
        # These commands don't have a fixed acceptable arguement length 
        printc("Invalid Syntax. Too many or too few arguments.", fail)

    elif len(args) > 0:
        func(args)
    
    else:
        func()

def operator(args):
    """
    Called when there is a possibility that args might be a combination
    of operators acting on BFs. Tries to simplifify it. 
    """
    check = False # Check if the operator is "=="
    for i in range(len(args)):
        if args[i] == "=" :
            if i != 0 and args[i-1] == "=":
                    check = True 
                    j = i # The index of the "==" operator

    if check: equal(args, j) # equality operator, a special case, is called
    else:
        commands = args.split()

        for i in range(len(commands)):
            if commands[i] in _workspace:
                # This is a BF
                exp = "(" + _workspace[commands[i]].expression() + ")"
                # Repacing the name with the actual expression
                commands[i] = exp

        new_exp = ""
        for i in commands:
            # Form the new BF
            new_exp += i + " "

        create_BF(new_exp)

# DigiCAD functions:

# Basic DigiCAD tools. These are the python functions called by the DigiCAD 
# commands. THESE ARE NOT THE ACTUAL DIGICAD COMMANDS! See the mapping in 
# command_list
def cls():  
    """
    Clears the terminal screen the terminal screen
    
    Source: http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def initialise():
    """
    Prints welcome flash message.
    """

    printc(
"""
************************************************************************
Welcome to DigiCAD, an engineering tool for doing numerous digital logic 
computations.

Developed by: Udey Rishi & Raghav Vamaraju (2014)

Run command "help" for opening up a list of all the commands. 

This is the command line interface. Run command "gui" if you intend to 
run the graphical user interface.
************************************************************************
"""
   , head)

def help_dc(args = None):
    """
    Calling it without any arguments will display the help of all the methods.
    Calling it with a command name gives the help regarding it.
    """
    if args:
        try:
            print("")
            command = args.strip()
            l1, l2 = help_dict[command]
            os.system("sed -n '%i,%i'p cli_help.txt" %(l1, l2))
        except KeyError:
            printc("'%s' is not a defined command." %command, fail)
    else:
        os.system("less cli_help.txt")

def workspace():
    """
    Displays all the variables defined in the current workspace.
    """
    if _workspace == {}:
        printc("Workspace is empty.", fail)
    else:
        j = 0
        for i in _workspace:
            printc("%s) %s" %(j, _workspace[i]))
            j += 1

def gui():
    """
    Launches GUI.
    http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-
    python-script-passing-in-args
    """
    os.system("python3 ./gui.py")

# Basic BF tools        
def create_BF(function):
    """
    Creates a Boolean Function and adds it to the current workspace.
    'function' is a string that can be parsed by the BF class.
    """
    try:
        symbols = ['*', '^', '%', '+', '-', 'v', "'", '~', "|"]

        test = find_name(function) # Check if user gave a proper name
        if not test: 
            test = find_name_hard(function) # Check if partial name is present

        # To prevent parsing-in reserved symbols        
        if test:
            for i in test:
                if i in symbols:
                    # A reserved letter was parsed in as the BF name. 
                    # Over-ride the user provided name.
                    test = None
                    break

        func = BF(function) # Creating the boolean function
        if test: func._name = test
        func_name = func.name() # Pulling out the user desired name

        if not test:
            # User did not give a name. So func_name is the self
            # generated name
            suffix = 0 # Added suffix to prevent collision
            while func_name in _workspace:
                # function name collision
                if suffix == 0:
                    # Just the first attempt, so add the suffix
                    func_name = func_name + str(suffix)
                else:
                    # Remove the old suffix first!
                    str_suff = str(suffix)
                    length = len(str_suff)
                    func_name = func_name[:-length] + str_suff
                suffix += 1

        while test and func_name in _workspace:
            # User inputted name is conflicting

            # Printing first so as to print in error colour
            printc("%s already exists in workspace. Overwrite? (Y/N)" \
                            %func_name, fail, " ")
            decision = input()

            if decision.lower() == 'y': test = False # Forcing continue
            else: 
                func_name = input("Please enter a new name: ")
        func._name = func_name # Changing the name of the BF
        _workspace[func_name] = func # Adding to workspace
        printc(func, blue) # Displaying the output as a confirmation

    except:
        printc("Please check the syntax.", fail)

def rename(arguments):
    """
    Renames a function in the workspace.
    """
    old, new = arguments.split()
    if old in _workspace:
        # BF exists in workspace
        temp = copy.deepcopy(_workspace[old])
        temp._name = new
        _workspace[new] = temp
        _workspace.pop(old)
        printc(_workspace[new]) # For visual confirmation

    else:
        printc("'%s' is not a BF in the current workspace!" %old, fail)

def del_bf(function = None):
    """
    Removes the BF from the workspace. If no argument is passed, empties the 
    workspace.
    """
    if function:
        # The user gave a specific function to be deleted
        function = function.strip()
        if function not in _workspace:
            # Invalid function
            printc("%s is not a BF in the workspace" %function, fail)

        else:
            printc("Are you sure you want to remove %s from the current workspace? (Y/N)" \
                       %function, fail, " ")
            decision = input()
            if decision.lower() == "y":
                _workspace.pop(function)
                printc("%s successfully removed from the workspace" %function, blue)
            else:
                printc("Nothing deleted", blue)

    else:
        printc("Are you sure you want to empty the current workspace? (Y/N)", \
                       fail, " ")
        decision = input()
        if decision.lower() == "y":
            _workspace.clear()
            printc("Workspace emptied!", blue)
        else:
            printc("Nothing deleted", blue)        

def expression(name):
    """
    Given a function name, returns the expression.

    Returns error if function name is not defined in the workspace.
    """
    if name in _workspace:
        printc(_workspace[name].expression())
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
         
def disp(name):
    """
    Given a BF name (defined in workspace, returns it).
    """
    printc(_workspace[name])
                
# The following functions connect CLI with the boolfunc module

# BF properties
def minterms(name):
    """
    Given a BF, returns the minterms.
    """    
    if name in _workspace:
        mint = _workspace[name].minterms()
        for i in range(len(mint)):
            if i != len(mint) - 1:
                printc("%i, " %mint[i], term = "")
            else:
                printc(mint[i])
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
                
def maxterms(name):
    """
    Given a BF, returns the maxterms.
    """    
    if name in _workspace:
        maxt = _workspace[name].maxterms()
        for i in range(len(maxt)):
            if i != len(maxt) - 1:
                printc("%i, " %maxt[i], term = "")
            else:
                printc(maxt[i])
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
         
def minterms_l(name):
    """
    Given a BF, returns the minterms in long form, i.e., grouped
    with number of 1's in it.
    """    
    if name in _workspace:
        mint = _workspace[name].mintermsl()
        for i in mint:
            category = mint[i]
            category.sort()
            printc("%i : %s" %(i, category))
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
                
def maxterms_l(name):
    """
    Given a BF, returns the minterms in long form, i.e., grouped
    with number of 1's in it.
    """    
    if name in _workspace:
        maxt = _workspace[name].maxtermsl()
        for i in maxt:
            category = maxt[i]
            category.sort()
            printc("%i : %s" %(i, category))
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
         
def BF_variables(name):
    """
    Given a BF name, returns the variables used in it.
    """
    if name in _workspace:
        var = _workspace[name].variables()
        var.sort()
        for i in range(len(var)):
            if i < len(var) - 1:
                printc("%s, " %var[i], term = "")
            else:
                printc(var[i])
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
                
def truth_table(name):
    """
    Given a BF name, returns its truth table.
    """
    if name in _workspace:
        # Making the title row
        var = _workspace[name].variables()
        variables = ""
        for i in var: variables += i + "-"
        variables = variables[:-1] # Removing the extra -
        printc("%s : Value" %variables, blue)

        # Generating the table
        table = _workspace[name].truthtable()
        # For sorting the result
        table_keys = list(table.keys())
        table_keys.sort(key = lambda x: int(x,2))
        for i in table_keys:
            printc("%s : %s" %(i, table[i]))
    else:
        printc("BF '%s'does not exist in the workspace" %name, fail)
         
# Operations
def equal(args, i = None):
    """
    Can be used in 2 cases:
    1. Called by operator (i != None)
    Called by the operator if "==" sign is detected.
    i and i-1 are the locations where "=" is found.

    2. Called by user i == None
    """
    if i:
        # Case 1
        args1 = args[:i-1].strip()
        args2 = args[i+1:].strip()

        if args1 in _workspace and args2 in _workspace:
            # Comparing and producing the result
            printc(_workspace[args1] == _workspace[args2])

        else:
            failed_arg = args1 if args1 not in _workspace else args2
            printc("%s is not a BF in the workspace" %failed_arg, fail)

    else:
        # Case 2
        funcs = args.split()

        check = True
        # Checking if all the parts of the arguments are BFs
        BF = []
        fail_list = ""
        for i in funcs:
            if i in _workspace: 
                # Finding the BFs and add it to the list
               BF.append(_workspace[i])  
            else:
                check = False
                fail_list += i + ", "

        if check:
            rv = True
            for i in range(len(BF)):
                if i > 0 and BF[i] != BF[i-1]:
                    rv = False
            printc(rv)
        else:
            fail_list = fail_list[:-2]
            printc("%s is(are) not BF(s) in the workspace" %fail_list, fail)

def standard_op(args, symbol):
    """
    The template function for operators or, and, xor, nor, and nand.
    """
    functions = args.split()
    bf = "" # The string Boolean function parsed

    # Checking the validity of the functions
    failed = ""
    check = True
    for i in functions:
        if i not in _workspace: 
            check = False
            failed += i + ", "
        else:
            bf+= "(%s) %s" %(_workspace[i].expression(), symbol)


    if check == False:
        failed = failed[:-2]
        printc("%s is(are) not a BF(s) in the workspace" %failed, fail)        

    else:
        bf = bf[:-2]
        create_BF(bf)

         
def OR(args):
    """
    Another way of finding the OR of functions. Just pass the sequence of
    BFs as args.
    """
    standard_op(args, "+")
         
def AND(args):
    """
    Another way of finding the AND of functions. Just pass the sequence of
    BFs as args.
    """
    standard_op(args, "*")
        
         
def XOR(args):
    """
    Another way of finding the XOR of functions. Just pass the sequence of
    BFs as args.
    """
    standard_op(args, "%")
        
def NOR (args):
    """
    Another way of finding the NOR of functions. Just pass the sequence of
    BFs as args.
    """
    standard_op(args, "-")
        
                
def NAND(args):
    """
    Another way of finding the NAND of functions. Just pass the sequence of
    BFs as args.
    """
    standard_op(args, "|")
        
def NOT(args):
    """
    Finds the not of the passed function. If more functions are passed,
    raises error.
    """
    function = args.strip()

    if function not in _workspace:
        printc("%s is not a BF in workspace" %function, fail)

    else:
        create_BF("~ (%s)" %_workspace[function].expression())

# Conversions/Calculations
def min_exp(function):
    """
    Returns the minterm expansion of the function.
    """
    if function.split()[0] in _workspace:
        # Find the BF, and add it to workspace
        rv = _workspace[function.split()[0]].min_expand()
        create_BF(rv._print())

    else:
        printc("%s is not a BF in workspace" %function.strip(), fail)

def max_exp(function):
    """
    Returns the maxterm expansion of the function.
    """
    if function.split()[0] in _workspace:
        # Find the BF, and add it to workspace
        rv = _workspace[function.split()[0]].max_expand()
        create_BF(rv._print())

    else:
        printc("%s is not a BF in workspace" %function.strip(), fail)
         
def sub(args):
    """
    Substitutes the value in the BF and returns the value.
    """
    arg_list = args.split()

    function = arg_list[0].strip() # The BF passed
    tt_value = arg_list[1].strip() # The binary number at which value is asked
    if function not in _workspace:
        printc("%s is not a BF in workspace" %function, fail)            
    else:
        try:
            printc(_workspace[function].sub(tt_value))
        except KeyError:
            printc("%s does not exist in the truthtable of %s" \
                  %(tt_value,function), fail)    

def minimise(function):
    """
    Returns the minimised sop form of the function.
    """
    if function.split()[0] in _workspace:
        # Find the min BF, and add it to the workspace
        rv = _workspace[function.split()[0]].min_sop()
        create_BF(rv._print())

    else:
        printc("%s is not a BF in workspace" %function.strip(), fail)

         
def num_ones(arg):
    """
    Returns the number of 1s in the binary form of a number.

    arg1 = number, arg2 = base (default 10)
    """
    arg_list = arg.split()
    if len(arg_list) < 2: arg_list.append("10") # Use default base 10
    
    try:
        number = arg_list[0]
        base = arg_list[1]
        printc(find_ones(int(number, int(base))))
    except ValueError:
        printc("Value is not a proper number in base-%s system!" %base, fail)
         
def num_zeros(arg):
    """
    Returns the number of 0s in the binary form of a number.

    arg1 = number, arg2 = bits, arg3 = base (default 10)
    """
    arg_list = arg.split()
    if len(arg_list) < 3: arg_list.append("10") # Use default base 10
    try:
        number = arg_list[0]
        bits = arg_list[1]
        base = arg_list[2]
        printc(find_zeros(int(number, int(base)), int(bits)))
    except ValueError:
        printc("Value is not a proper number in %s system!" %base, fail)
         
                
def binary(arg):
    """
    Returns the binary notation of the number.

    arg1 = number, arg2 = # of bits, arg3 = base (default 10)
    """
    arg_list = arg.split()
    if len(arg_list) < 3: arg_list.append("10") # Use default base 10
    try:
        number = arg_list[0]
        bits = arg_list[1]
        base = arg_list[2]
        printc(bin_conv(int(number, int(base)), int(bits)))
    except ValueError:
        printc("Value is not a number!", fail)       
         
# DigiCAD CLI Variables:

# Contains all the commands as objects
command_list = { # Basic DigiCAD commands
                'clear' : cls, 
                'flash' : initialise, 
                'help' : help_dc,
                'workspace' : workspace,
                'gui' : gui,
                # Basic BF tools
                'def' : create_BF, 
                'rename' : rename,
                'expression' : expression, 
                'display_BF' : disp,
                'del' : del_bf,
                # BF properties
                'minterms' : minterms,
                'maxterms' : maxterms, 
                'mintermsl' : minterms_l,
                'maxtermsl' : maxterms_l, 
                'variables' : BF_variables,
                'truthtable' : truth_table, 
                # Operations
                'equal': equal, 
                'or' : OR, 
                'and' : AND, 
                'xor' : XOR,
                '~' : NOT,
                'not' : NOT, 
                'nor' : NOR ,
                'nand' : NAND,
                # Conversions/Calculations
                'min_exp' : min_exp,
                'max_exp' : max_exp, 
                'sub' : sub,
                'minimise' : minimise, 
                'num_ones' : num_ones, 
                'num_zeros' : num_zeros,
                'binary' : binary
                } 

# Stores how many arguments a command expects
arg_len = {
            'clear' : [0], 
            'flash' : [0], 
            'help' : [0, 1],
            'workspace' : [0],
            'gui' : [0],
            'def' : [], # don't care 
            'rename' : [2],
            'expression' : [1], 
            'display_BF' : [1],
            'del' : [0,1],
            'minterms' : [1],
            'maxterms' : [1], 
            'mintermsl' : [1],
            'maxtermsl' : [1], 
            'variables' : [1],
            'truthtable' : [1], 
            'equal': [], # don't care 
            'or' : [], # don't care ]
            'and' : [], # don't care  
            'xor' : [], # don't care  
            '~' : [1],
            'not' : [1], 
            'nor' : [], # don't care 
            'nand' : [], # don't care 
            'min_exp' : [1],
            'max_exp' : [1], 
            'sub' : [2],
            'minimise' : [1], 
            'num_ones' : [1,2], 
            'num_zeros' : [2,3],
            'binary' : [2,3]
        }

# Contains the line numbers of the help documentation
help_dict = {
            'clear' : (32, 35), 
            'flash' : (38, 40), 
            'help' : (43, 49),
            'workspace' : (52, 54),
            'gui' : (57, 62),
            'def' : (65, 77),
            'rename' : (241, 245),
            'expression' : (80, 86), 
            'display_BF' : (89,92),
            'del' : (95,99),
            'minterms' : (102,106),
            'maxterms' : (109,113), 
            'mintermsl' : (116,121),
            'maxtermsl' : (124,129),
            'variables' : (132,136),
            'truthtable' : (139, 143), 
            'equal': (146,151), 
            'or' : (154,158),
            'and' : (161,165),
            'xor' : (168,172),
            '~' : (175, 180),
            'not' : (175,180), 
            'nor' : (183,185),
            'nand' : (188,190), 
            'min_exp' : (193,195),
            'max_exp' : (198,200), 
            'sub' : (203,207),
            'minimise' : (210,216), 
            'num_ones' : (219,223), 
            'num_zeros' : (226,231),
            'binary' : (234,239)
        }
