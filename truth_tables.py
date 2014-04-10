from strings import *

def make_table(expression):
    """
    Given a Boolean expression in the form:
    
    "f(a, b, c, d) = (a + ~b|(c - d))*(b^c)...."
    
    make_table returns a truth table; that is, a dictionary mapping strings of
    possible values for the variables to the value of the function using those
    values. Refer to the docstrings in strings.py for the correct input format.
    For example:
    
    >>> make_table("f(a, b) = a % b")
    {'00': False, '01': True, '10': True, '11': False}

    >>> make_table("f(a, b) = a * b")
    {'00': False, '01': False, '10': False, '11': True}

    >>> make_table("f(a, b) = a + b")
    {'00': False, '01': True, '10': True, '11': True}

    >>> make_table("f(a, b) = a * ~b")
    {'00': False, '01': False, '10': True, '11': False}
    """
    
    # Extract the variables and the function itself from the expression.
    vars, f = parse(expression) 
    f_clean = f.replace('^', '%')
    
    # Create the truth_table variable (a dictionary).
    truth_table = {}
    
    # Find the number of variables in the expression.
    num_vars = len(vars)
    
    # Find the number of rows in the truth table.
    rows = int(2**num_vars)
    
    # Create a string that can be used to print numbers in binary.
    bin_str = '{0:0' + str(num_vars) + 'b}'
    
    # For each row in the truth table, evaluate the function and store its value.
    for row in range(0, rows):
    
        # Find the binary equivalent of the row number.
        # Each digit in this binary number corresponds to a value for a variable.
        binary_num = bin_str.format(row)
        
        # Create a temporary copy of the function.
        f_temp = f
        
        # Create a temporary counter.
        i = 0
        
        # Replace each variable in the function with its corresponding binary
        # value (based on the row in the truth table). 
        for var in vars:
            f_temp = f_temp.replace(var, binary_num[i])
            i += 1
            
        # Replace each operator with corresponding keywords (and, or, not).
        f_temp = f_temp.replace('|', "' or ~")
        f_temp = f_temp.replace('-', "' and ~")
        f_temp = f_temp.replace('*', ' and ')
        f_temp = f_temp.replace('+', ' or ')
        f_temp = f_temp.replace('v', ' or ')
        f_temp = f_temp.replace('~', ' not ')
        f_temp = special_replace(f_temp, "'", ' not ')
        
        # Determine the truth value of the function and store it.    
        truth_table[binary_num] = bool(eval(f_temp))
        
    return vars, truth_table, f_clean
        
        
        
        
        
        
        
    
