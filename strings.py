def parse(s):
    """
    Function to parse a string containing a Boolean expression and divide it
    into useful parts. 

    Expressions are expected to be in the form:
        
    "f(a, b, c, d) = (a + b(c + d))(bc)....etc.
    """
    
    length = len(s) - 1
    for letter in s:
        
