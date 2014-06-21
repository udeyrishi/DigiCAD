"""
The string parsing module. Contains functions used by boolfunc for helping 
recognise the user input.
Developed by: Udey Rishi & Raghav Vamaraju, 2014
"""

def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Returns a list of variables used in the function and a string containing the 
    function. 
    
    The user can input a Boolean expression using different symbols for 'AND', 'OR',
    etc. (listed below), but the output will only use one set of symbols. 
    
    The default set of symbols used IN THE OUTPUT are:
    
    Output Symbol       Operator
    '*'                 'AND'
    '+'                 'OR'
    '~'                 'NOT'
    '%'                 'XOR'
    '|'                 'NAND'
    '-'                 'NOR'

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a' + ~b*(c v d))'*(b^c%d' - a | b)...."etc.

    "f" can be any name. The variable names can be anything, but brackets, spaces, dots, *, 
    /, \, ^, v, ', ~, &, +, |, %, and - symbols will be removed. (Basically, variables should be
    a combination of letters and/or numbers containing no special characters). Variables must 
    be separated by commas, and cannot contain commas within their names. The list of variables 
    must be enclosed by brackets (as in the example above). The expression must contain an 
    equal ("=") sign.
    
    Symbol usage for an INPUT:
    
    Input Symbol        Operator
    '*'                 'AND'
    '^'                 'AND'
    '+'                 'OR'
    'v'                 'OR'
    "'"                 'NOT'
    '~'                 'NOT'
    '%'                 'XOR'
    '|'                 'NAND'
    '-'                 'NOR'
    
    All symbols can be used interchangeably in a function definition. For example:
    "f(a, b) = a^b*a + ~a*b'"
    is a valid function definition.
    
    parse("f(a, b) = a^b*a + ~a*b'") is valid usage of the function parse().
    
    To create a Boolean function, run "boolfunc.py" to initiate the Boolean Function (BF) class.
    Example:
    "new_function = BF("f(a, b) = a+b")"
    will create the function 'a+b'. There are various methods you can use on this as part of the BF class.
    
    Terms should be enclosed with appropriate brackets in the input function.
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
    function = special_replace(function, "'", '~')
    
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

    # Delete unnecessary brackets in the function.
    function = delete_brackets(function)

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
    bracket_counter = 0
    
    # If the list of indices is not empty, iterate through the list.
    # For each character, check if it is preceded by a bracket. If so, 
    # find its corresponding bracket (backwards) and move the character
    # there. Otherwise, just move the character one space backwards.
    if character_indices != []:
        for character in character_indices:
            if s[character-1] == ')':
                left_bracket = character - 2
                
                # Find the left bracket corresponding to the current right bracket.
                while s[left_bracket] != '(' or bracket_counter:
                    if s[left_bracket] == ')':
                        bracket_counter += 1
                    elif s[left_bracket] == '(':
                        bracket_counter -= 1
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
    
 

def delete_brackets(s):
    """
    Returns a copy of the string s with unnecessary brackets removed.
    Unnecessary brackets are layers of brackets that enclose the same term.
    For example:
    
    >>> s = '(((a)))'
    >>> delete_brackets(s)
    '(a)'
    
    >>> s = 'a + ((b + c)) + ((~c))'
    >>> delete_brackets(s)
    'a + (b + c) + (~c)'
    """
    
    # Index keeps track of the position in the string.
    # removal_list is a list of bracket characters that need to be removed.
    # Decrement is an offset used when removing the brackets.
    index = 0
    removal_list = []
    decrement = 0
    
    # Walk through each character in s and look for left bracket characters. 
    # If two of them are side-by-side, AND the two corresonding right brackets
    # are side-by-side, add the pair to the list of brackets that need to be removed.
    for char in s:
        if char == '(' and s[index+1] == '(':
            if (corresponding_bracket(s, index) - 1) == corresponding_bracket(s, index+1):
                removal_list.append(index)
                removal_list.append(corresponding_bracket(s, index))
        index += 1
    
    # Sort the removal_list. This way, the list can be iterated from left to right.
    removal_list.sort()
    
    # Remove brackets one at a time. Each time a bracket is removed, the index of
    # subsequent brackets decrease by one (since the size of s has decreased).
    for index in removal_list:
        s = remove(s, index-decrement)
        decrement += 1
        
    return s
    
    

def corresponding_bracket(s, bracket):
    """
    Given the index of a left or right bracket character, return the
    index of the correspoding bracket character in s. Assumes that all
    brackets are enclosed properly. Returns None if the index of a 
    bracket is not given.
    
    Examples:
    
    >>> s = '(((a)))'
    >>> correspoding_bracket(s, 0)
    6
    
    >>> s = '(((a)))'
    >>> correspoding_bracket(s, 6)
    0
    
    >>> s = '(((a)))'
    >>> correspoding_bracket(s, 5)
    1
    
    >>> s = '(((a)))'
    >>> correspoding_bracket(s, 3)
    None
    
    >>> s = 'a + ((b + c)) + ((~c))'
    >>> correspoding_bracket(s, 5)
    11
    """
    
    # If the given index in s is not an index of a bracket character, return None.
    if s[bracket] != '(' and s[bracket] != ')':
        return None
        
    bracket_counter = 0    
        
    # If the character is a left bracket, find the corresponding right bracket
    # by searching forward in the string. If another left bracket is found, ignore
    # the next right bracket.
    if s[bracket] == '(':
        bracket += 1
        while s[bracket] != ')' or bracket_counter:
            if s[bracket] == '(':
                bracket_counter += 1
            elif s[bracket] == ')':
                bracket_counter -= 1
            bracket += 1    
    
    # If the character is a right bracket, find the corresponding left bracket
    # by searching backward in the string. If another right bracket is found, ignore
    # the next left bracket.    
    elif s[bracket] == ')':
        bracket -= 1
        while s[bracket] != '(' or bracket_counter:
            if s[bracket] == ')':
                bracket_counter += 1
            elif s[bracket] == '(':
                bracket_counter -= 1
            bracket -= 1    
            
    return bracket        
    
    
    
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
    
    

def remove(s, i):
    """
    Returns the string s with the character at index i removed.
    
    Examples:
    
    >>> s = '12304'
    >>> remove(s, 3)
    '1234'
    
    >>> s = '0123'
    >>> remove(s, 0)
    '123'

    >>> s = '0123'
    >>> remove(s, 3)
    '012'
    
    >>> s = '0123'
    >>> remove(s, -1)
    '0123'
    
    >>> s = '0123'
    >>> remove(s, 4)
    '0123'
    """
    
    # If the index is out of range, return the original string.
    if i < 0 or i >= len(s):
        return s
    
    return s[:i] + s[i+1:]
    
def myindexreturner(string, character):
    """
    Returns a list containing the indices of "character" in "String"
    """
    rv = []
    for i in range(len(string)): 
        if string[i] == character: rv.append(i)
    return rv
  
    
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
        # Separating expression from everything else
    if "=" in function:
        expression = function[function.index("=") + 1:].strip()
        everything_else = function[:function.index("=")].strip()

    else:
        expression = function.strip()
        everything_else = ""

    # Parsing everything_else
    variables = set()
    if everything_else == "":
        function_name = name

    elif "(" in everything_else and ")" in everything_else:
        function_name = everything_else[:everything_else.index("(")].strip()
        possible_variables = everything_else[everything_else.index("(") + 1:\
                                             everything_else.index(")")].strip()
        possible_variables = possible_variables.split(",")
        variables = {i.strip() for i in possible_variables}

    else:
        function_name = everything_else.replace("(", "")
        function_name = function_name.replace(")", "")
        function_name = function_name.replace(",", "")
        function_name = function_name.replace(" ", "")

    # Parsing out variables from expression
    symbols = ['*', '^', '%', '+', '-', 'v', "'", '~', "|"]
    symbol_indices = []
    for symbol in symbols:
        if symbol in expression:
            indices = myindexreturner(expression, symbol)
            for i in indices:
                symbol_indices.append(i)
    symbol_indices.sort()
    
    start = 0
    for index in symbol_indices:
        variable = expression[start:index].strip().replace("(", "").replace(")", "")
        variables = variables.union({variable})
        start = index+1

    variable = expression[start:].strip().replace("(", "").replace(")", "")
    variables = variables.union({variable})

    # Forming the function
    variables = list(variables)
    variables.sort()
    rv = "%s%s = %s" %(function_name, tuple(variables), expression)
    rv = rv.replace("'", "")
    return rv

        
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


a = proper("foo(b,a) = (a+b) + (a*b)")