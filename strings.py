def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Returns a list of variables used in the function, a string containing the 
    function, and a list of symbols that the user used in the function. 
    The list of symbols will always be in a particular order; it will always 
    start with the symbol for 'AND', followed by 'OR', 'NOT', and 'XOR', 'NAND', and 'NOR'.
    By default, symbols will be the following:
    
    symbols = ['*', '+', "'", '^', '|', '-']

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a' + ~b*(c v d))'*(b^c&d' - a | b)...."etc.

    "f" can be any name. The variable names can be anything, but brackets, spaces, dots, *, 
    /, \, ^, v, ', ~, &, +, |, and - symbols will be removed. (Basically, variables should be
    a combination of letters and/or numbers containing no special characters). Variables must 
    be separated by commas, and cannot contain commas within their names. The list of variables 
    must be enclosed by brackets (as in the example above). The expression must contain an 
    equal ("=") sign.
    
    Symbol usage:
    
    Symbol      Operator
    '*'         'AND'
    '&'         'AND'
    '+'         'OR'
    'v'         'OR'
    "'"         'NOT'
    '~'         'NOT'
    '^'         'XOR'
    '|'         'NAND'
    '-'         'NOR'
    
    All symbols can be used interchangeably in a function definition.
    """
    
    position = -1
    variables = []
    symbols = ['*', '+', "'", '^', '|', '-']
    
    # Walk through each character in the string while keeping track of the position.
    # Stop once you find the end of the function arguments.
    for char in s:
        position += 1

        # If the character is a left bracket, record its position. 
        if char == '(':
            bracket1 = position
        
        # If the character is a right bracket, record its position.
        elif char == ')':
            bracket2 = position
          
        # If the character is an equal sign, record its position and exit the search.
        elif char == '=':
            equals = position
            break
            
    # Extract the slice of the string within the brackets (the arguments). 
    arguments = s[bracket1+1 : bracket2]
    
    # Store the original variable names in a list.
    orig_vars = arguments.split(',')
    
    # Delete all unwanted characters from the arguments.
    arguments = arguments.translate(str.maketrans('','',"()[]{} .*/\^v'~+&|-"))
    
    # Make a new list of variable names (with unwanted characters removed).
    variables = arguments.split(',')
    
    # The function is everything beyond the equals sign.
    function = s[equals+1:]
    
    i = -1
    # In the function, replace the original variable names with the new names.
    for orig_var in orig_vars:
        i += 1
        function = function.replace(orig_var, variables[i])
        
    # Replace unnecessary brackets in the function.
    function = function.translate(str.maketrans('[]{}','()()',' '))
    
    i = -1
    # If the user used the following symbols, then update the list.
    for symbol in ['&', 'v', '~']:
        i += 1
        if symbol in function:
            symbols[i] = symbol
    
    #for nand and nor, create a functio nthat finds brackets. (first, find all
    # nand/not symbols and iterate over those locatios). if there is a
    #nand or nor symbol, add brackets around that entire term...
    
    return variables, function, symbols

    

def find_all(s, ss):
    """
    A helper function used in creating truth tables (truth_tables.py).
    Finds all occurrences of substring ss in string s. 
    Returns a list of starting indices of ss in s. If there is no instance
    of ss in s, find_all returns an empty list.

    Example:
    
    >>> s = "132435132435"
    >>> find_all(s, "3")
    [1, 4, 7, 10]
    
    >>> s = "cat1 and cat2 were best friends."
    >>> find_all(s, "cat")
    [0, 9]    
    
    >>> s = " hello world, world hello"
    >>> find_all(s, "hello")
    [1, 20]     

    >>> s = " hello world, world hello"    
    >>> find_all(s, "l")
    [3, 4, 10, 17, 22, 23]
   
    >>> s = "abc"
    >>> find_all(s, "z")
    []
    
    >>> s = "abc"
    >>> find_all(s, "abcd")
    []
    """
    
    # If s is empty, return an empty list.
    if len(s) == 0:
        return []
    
    # If ss is empty, return an empty list.
    if len(ss) == 0:
        return []
    
    # Initialize the list of indices.
    indices = []
    
    # Find the size of the string.
    size = len(s)
    
    # Find the size of the sub-string.
    size_ss = len(ss)
    
    # For every index in s, check if s[index:index+size_ss] = ss. 
    # If so, append index to the list of indices.
    for index in range(size-size_ss+1):
        if s[index:index+size_ss] == ss:
            indices.append(index)
   
    return indices
    
    
    
def special_replace(s, c, replacor):
    """
    A helper function used in creating truth tables (truth_tables.py).
    Returns the string s with the character c "special replaced" by the replacor.
    Assuming s is a Boolean function, special_replace will move the character c
    before the term preceeding it, and then replace it by the replacor.
    
    Examples:
    
    >>> s = "f(a, b, c, d) = (a+b+c)'"
    >>> special_replace(s, "'", " not ")
    "f(a, b, c, d) =  not (a+b+c)"
    
    >>> s = "f(a, b, c, d) = (a+b'+c)'"
    >>> special_replace(s, "'", "'")
    "f(a, b, c, d) = '(a+'b+c)"    
    
    >>> s = "f(a, b, c, d) = (a'+b'+c)'"
    >>> special_replace(s, "'", " not ")
    "f(a, b, c, d) =  not ( not a+ not b+c)"  

    """
    
    # Search for the indices of c in s.
    character_indices = find_all(s, c)
        
    # If the list of indices is not empty, iterate through the list.
    # For each character, check if it is preceded by a bracket. If so, 
    # find its corresponding bracket (backwards) and move the character
    # there. Otherwise, just move the character one space backwards.
    if character_indices != []:
        for character in character_indices:
            if s[character-1] == ')':
                left_bracket = character - 2
                # Find the left bracket.
                while s[left_bracket] != '(':
                    left_bracket -= 1
                # Create the new string.
                s = s[:left_bracket] + c + s[left_bracket:character] + s[character+1:]
               
            else: 
                # Reposition the character one space backwards in the string.
                s = s[:character-1] + c + s[character-1] + s[character+1:]
           
        # Now that every c has been repositioned, replace each c with the replacor.
        s = s.replace(c, replacor)

    return s
    

def proper(function, name = "f"):
    """
    Given a Boolean function (just expression without f(...) notation), converts
    it to standard notation that parse can understand. Can be used as a helper
    with parse.

    This has the caability of handline only 2 cases, both of which are logically 
    correct, but just use different semantics.

    e.g. "a + b*c" == "f(a,b,c) = a + b*c"
    It returns a standard string "f(a, b, c) = a + b*c" in this case.
    
    By default, the function generated is f.

    >>> proper("a+b*c")
    'f(a, b, c) = a+b*c'
    
    >>> proper("f(a,b,c) = a+b*c")
    'f(a,b,c) = a+b*c'

    >>> proper('f = a+b+c')
    'f(a, b, c) = a+b+c'

    >>> proper('f(a,b,c = a+b+c')
    'fabc(a, b, c) = a+b+c'
    
    >>> proper('fa,b,c) = a+b+c')
    'fabc(a, b, c) = a+b+c'

    >>> proper('f   a,b,c) = a+b+c')
    'fabc(a, b, c) = a+b+c'

    >>> proper('f  a,b,c)=a+b+c')
    'fabc(a, b, c) = a+b+c'
    """
    variables = set() # All the variables found in the expression
    trash = list() # Everything else that is found in the expression

    # Just for backing up the order. There is a possibility that the given
    # function was partially proper.
    possible_name = "" 


    index = 0
    flag = 0 # Flag for the case where just function name was given without vars

    for c in function:
        if c == "=":
            if ")" in trash and "(" in trash:
                # Proper notation was passed in. Ignore the variables set and return
                # the function itself
                return function 
            else:
                # Function name was given without listing variables
                # Partially proper syntax. Set the flag
                flag = 1
                break
        else: 
            if 97 <= ord(c) <= 122 or 65 <= ord(c) <= 90:
                # c is an english letter, so a variable, or part of name (partially proper case)
                variables.add(c)
                possible_name += c

            else:
                trash.append(c)
        index += 1

    if flag == 1:
        # Chop off the function name, and pass it separately in a recursive call
        if function[index+1] == ' ':
            # If spacing was used after "="
            return proper(function[index+2:], possible_name)
        else:
            # If spacing wasn't used after "="
            return proper(function[index+1:], possible_name)
    
    else:
        # Sort the variables alphabetically

        variables = list(variables)
        variables.sort()

        var_string = ""
        for i in variables:
            var_string += i + ", "
        var_string = var_string[:-2]         

        return ("%s(%s) = %s" %(name, var_string, function))

def find_name(function):
    """
    Given a function string in the proper format, traces out the name of the 
    function.

    >>> find_name("f(a,b,c) = a+b+c")
    'f'

    >>> find_name("apple(a,e,g) = ~a")
    'apple'
    """
    rv = ""
    for c in function:
        if c != "(": 
            rv += c
        else:
            return rv
    
    
    
    
    
    
    
    