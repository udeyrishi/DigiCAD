def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Returns a list of variables used in the function and a string containing the 
    function. 
    
    The user can input a Boolean expression using different symbols for 'AND', 'OR',
    etc. (listed below), but the output will only use one set of symbols. 
    The default set of symbols used in the output are:
    
    Symbol      Operator
    '*'         'AND'
    '+'         'OR'
    '~'         'NOT'
    '%'         'XOR'
    '|'         'NAND'
    '-'         'NOR'

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a' + ~b*(c v d))'*(b^c&d' - a | b)...."etc.

    "f" can be any name. The variable names can be anything, but brackets, spaces, dots, *, 
    /, \, ^, v, ', ~, &, +, |, %, and - symbols will be removed. (Basically, variables should be
    a combination of letters and/or numbers containing no special characters). Variables must 
    be separated by commas, and cannot contain commas within their names. The list of variables 
    must be enclosed by brackets (as in the example above). The expression must contain an 
    equal ("=") sign.
    
    Symbol usage:
    
    Symbol      Operator
    '*'         'AND'
    '^'         'AND'
    '+'         'OR'
    'v'         'OR'
    "'"         'NOT'
    '~'         'NOT'
    '%'         'XOR'
    '|'         'NAND'
    '-'         'NOR'
    
    All symbols can be used interchangeably in a function definition.
    """
    
    position = -1
    variables = []
    
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
    arguments = arguments.translate(str.maketrans('','',"()[]{} .*/\^v'~+&|-%"))
    
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
        
    # For the output, use only a specifc set of symbols.
    function = function.replace('^', '*')
    function = function.replace('%', '^')
    function = function.replace('v', '+')
    function = special_replace(function, "'", ' not ')
    function = function.replace(' not ', "~")
    
    # Find all 'NOR', 'NAND, and 'XOR symbols and enclose those terms 
    # with brackets. Walk through the function one character at a time 
    # from left to right to preserve order of operations.
    pos = 0
    while pos < len(function):
        if function[pos] == '^':
            function = enclose(function, pos+1)
            function = enclose(function, pos)
            pos += 1
        elif function[pos] in {'-', '|'}:
            function = enclose(function, pos)
            pos += 1
        pos += 1    
    """    
    pos = 0    
    while pos < len(function):
        if function[pos] == '^':
            function = enclose(function, pos)
            pos += 1
        pos += 1              
    """
    return variables, function

    

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
    

    
def enclose(f, pos, left_enclosure='(', right_enclosure=')'):
    """
    A helper function used in parsing Boolean functions (strings.py).
    Given a Boolean function string, f, and a position in that string, 
    pos, enclose() will return f with the terms surrounding pos 
    enclosed in the left and right enclosures. 
    
    Examples:
    
    >>> f = "a|b"
    >>> enclose(f, 1, '(', ')')
    '(a|b)'
    
    >>> f = "(a+b)*(a+c)"
    >>> enclose(f, 5, '(', ')')
    '((a+b)*(a+c))'
    
    >>> f = "(a+b)*a"
    >>> enclose(f, 5, '(', ')')
    '((a+b)*a)'
    
    >>> f = "a+b*(a+(c*d))"
    >>> enclose(f, 3, '(', ')')
    'a+(b*(a+(c*d)))'
    """
    
    # Find the characters adjacent to pos.
    left_pos = pos - 1
    right_pos = pos + 1
    
    # Define all of the possible operators in the function.
    symbols = {'*', '^', '+', 'v', '%', '|', '-'}
        
    # If the left position is a 'NOT' symbol, move back one space.    
    while f[left_pos] == "'":
        left_pos -= 1    
    
    increment = 0
    # If the position left of pos is not a bracket, then find the nearest
    # symbol and enclose from there.
    if f[left_pos] != ')':
        increment += 1
        while f[left_pos] not in symbols and left_pos != -1:
            left_pos -= 1
    
    # If the position left of pos is a bracket, then find the corresponding
    # bracket and enclose from there.
    elif f[left_pos] == ')':
        bracket_counter = 1
        while f[left_pos] != '(' or bracket_counter != 0:
            left_pos -= 1
            if f[left_pos] == ')':
                bracket_counter += 1
            elif f[left_pos] == '(':
                bracket_counter -= 1

    f = insert(f, left_enclosure, left_pos+increment)
     
    # f has now changed; update the pointer to the new right-position.
    right_pos += 1

    # If the right position is beyond the range of the string, insert the bracket at the end.
    if right_pos >= len(f):
        f = insert(f, right_enclosure, len(f))
        return f
    
    # If the right position is a 'NOT' symbol, move forward one space.    
    while f[right_pos] == "~":
        right_pos += 1 
        
    # If the position right of pos is not a bracket, then find the nearest
    # symbol and enclose from there.
    if f[right_pos] != '(':
        while right_pos != len(f) and f[right_pos] not in symbols:
            right_pos += 1
        f = insert(f, right_enclosure, right_pos)    

    # If the position right of pos is a bracket, then find the corresponding
    # bracket and enclose from there.
    elif f[right_pos] == '(':
        bracket_counter = 1
        while f[right_pos] != ')' or bracket_counter != 0:
            right_pos += 1
            if f[right_pos] == '(':
                bracket_counter += 1
            elif f[right_pos] == ')':
                bracket_counter -= 1
        f = insert(f, right_enclosure, right_pos)
        
    return f
    
    
    
def insert(s, c, pos):
    """
    Returns the string s with character c inserted into position pos.
    c can also be a string. If the position given is 0, c will be placed
    at the beginning of the string. If the position given is len(s), c
    will be placed at the end of the string. If pos is anything beyond these
    bounds, insert() returns None.
    
    Examples:
    
    >>> s = "134"
    >>> insert(s, 2, 1)
    "1234"
    
    >>> s = "134"
    >>> insert(s, 5, 3)
    "1345"
    
    >>> s = "134"
    >>> insert(s, 0, 0)
    "0134"
    
    >>> s = "134"
    >>> insert(s, 'a', 2)
    "13a4"
    """
    
    # If the position is zero, return s with c prepended.
    if pos == 0:
        return str(c) + s
        
    # If the position is len(s), return s with c appended.
    elif pos == len(s):
        return s + str(c)
        
    # If the position is between 0 and len(s), return s with c attached at pos.
    elif 0 < pos < len(s):
        return s[:pos] + str(c) + s[pos:]
    
    # If the position is not within these bounds, return None.
    else:
        return None
    
    
    
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
    
    