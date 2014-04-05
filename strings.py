def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Returns a list of variables and a string containing the function.

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a + ~b*(c + d))*(b^c)...."etc.

    "f" can be any name. The variables names can be anything, but brackets, spaces, dots, *, 
    /, \, ^, and + symbols will be removed. Variables must be separated by commas, and cannot contain 
    commas within their names. The list of variables must be enclosed by brackets (as in the example 
    above). The expression must contain an equal ("=") sign.
    
    '+' symbols are used for 'OR'. '*' symbols are used for AND. '^' symbols are used for 'XOR'.
    '~' symbols are used for 'NOT'.
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
    # Delete all unwanted characters.
    arguments = s[bracket1+1 : bracket2]
    arguments = arguments.translate(str.maketrans('','','()[]{} .*/\^+'))
    
    # Variables is a list of the variable names (as strings).
    variables = arguments.split(',')
    
    # The function is everything beyond the equals sign.
    function = s[equals+1:]
    
    # Replace/Delete unnecessary characters in the function.
    function = function.translate(str.maketrans('[]{}','()()',' '))
    
    return variables, function



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