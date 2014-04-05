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

    
