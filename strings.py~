def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Returns a list of variables, a list of terms, 

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a + b(c + d))(bc)...."etc.

    "f" can be any name. The variables can be anything, but brackets, spaces, and dots will be removed. 
    Variables must be separated by commas, and the list of variables must be enclosed 
    by brackets (as in the example above). The expression must contain an equal ("=") sign.
    """
    
    length = len(s) - 1
    position = -1
    variables = []

    
    # Walk through each character in the string while keeping track of the position.\
    # Stop once you find the end of the function arguments.
    for char in s:
        position += 1

        # If the character is a left bracket, record its position. 
        if char == '(':
            1st_bracket = position
        
        # If the character is a right bracket, record its position and exit the search.
        elif char == ')':
            2nd_bracket = position
            break


    arguments = s[1st_bracket+1, 2nd_bracket]
    arguments = arguments.replace(' ', '')
    variables = arguments.split(',')
    


