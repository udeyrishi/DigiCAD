"""
The Boolean Function module for the DigiCAD.
Runs the under-the-hood Boolean algebra required by it.

The K-map is based on the Quine-McCluskey algorithm (instead of the traditional 
matrix form).
"""

from truth_tables import *
import copy

class InvalidBooleanFunctionError(Exception):
    pass

class BF:
    """
    Creates a boolean function 
    """

    def __init__(self, function, name = 'f', dc=None):

        # This name is useless if the function is in proper form
        # If not in proper form, this name will be applied
        function = proper(function, name)

        # After appropriate name is set up, store this name as an attribute
        self._name = find_name(function)

        # Parsing out the list of variables in the expression and creating the
        # truth table
        variables, table = make_table(function)
        
        minterms = [i for i in table if table[i]]
        maxterms = [i for i in table if not table[i]]

        # Testing consistency of # of expressions
        okay = test_vals(minterms)
        if not okay: 
            raise InvalidBooleanFunctionError("Inconsistent number of expressions")

        okay = test_vals(maxterms)
        if not okay:
            raise InvalidBooleanFunctionError("Inconsistent number of expressions")

        if len(variables) != len(minterms[0]):
            raise InvalidBooleanFunctionError("Inconsistent number of expressions")
        
        # Everything is good so store the vars, TT and the expression
        self._expression = function
        self._variables = variables
        self._table = table

        # Storing minterms hashed with the number of 1s
        self._minterms = {}

        # Converting the string buts into numerical bit lists
        minterms2 = list()

        for i in minterms:
            minterms2.append(int(i, 2))

        for i in minterms2:
            if find_ones(i) in self._minterms:
                self._minterms[find_ones(i)].append(i)
            else:
                self._minterms[find_ones(i)] = [i]

        # Storing minterms hashed with the number of 1s
        self._maxterms = {}

        # Move this functionality directly into minterm generation later
        maxterms2 = list()

        for i in maxterms:
            maxterms2.append(int(i, 2))

        for i in maxterms2:
            if find_zeros(i, len(variables)) in self._maxterms:
                self._maxterms[find_zeros(i, len(variables))].append(i)
            else:
                self._maxterms[find_zeros(i, len(variables))] = [i]

        if dc:
            # Testing consistency of # of expressions
            okay = test_vals(dc)
            if not okay: raise InvalidBooleanFunctionError("Inconsistent number of expressions")

            # Testing consistency of # of expressions
            for i in dc:
                if sum(i) in self._dc:
                    self._dc[sum(i)].append(i)
                else:
                    self._dc[sum(i)] = [i]

    def minterms(self):
        rv = []
        for i in self._minterms.values():
            rv += i 
        return rv

    def mintermsl(self):
        return copy.deepcopy(self._minterms)

    def maxterms(self):
        rv = []
        for i in self._maxterms.values():
            rv += i 
        return rv

    def maxtermsl(self):
        return copy.deepcopy(self._maxterms)

    def variables(self):
        return copy.deepcopy(self._variables)

    def truthtable(self):
        return copy.deepcopy(self._table)

    def __str__(self):
        return copy.deepcopy(self._expression)

    def __repr__(self):
        return copy.deepcopy(self._expression)

    def __eq__(self, func):
        try:
            return self.truthtable() == func.truthtable()
        except AttributeError:
            raise InvalidBooleanFunctionError("Object isn't a Boolean Function!")

    def sop(self):
        """
        Returns the s-o-p form of the boolean function.
        """
        rv = ""
        for num_minterm in self.minterms():

            # Converting numerical minterm to binary form for bitwise checks
            minterm = bin_conv(num_minterm, len(self.variables()))

            # Starting the next term
            if len(rv): term = " + "
            else: term = ""

            # Checking all the bits of that minterm and forming the term
            for i in range(len(self.variables())):
                if term != " + " and term != "": term += "*"
                if int(minterm[i]):
                    term += self.variables()[i]
                else:
                    term += "~" + self.variables()[i]
            rv += term
        
        variables = ""
        for i in self.variables():
            variables += i + ", "
        variables = variables[:-2]

        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._expression = ("f(%s) = %s" %(variables, rv))
        return rv2        
                    
    def pos(self):
        """
        Returns the p-o-s form of the boolean function.
        """
        rv = ""
        for num_maxterm in self.maxterms():

            # Converting numerical maxterm to binary for for bitwise checks
            maxterm = bin_conv(num_maxterm, len(self.variables()))

            # Starting the next factor
            if len(rv): factor = " * ("
            else: factor = "("

            # Checking all the bits of that maxterm and forming the factor
            for i in range(len(self.variables())):
                if factor != " * (" and factor != "(": factor += " + "
                if int(maxterm[i]):
                    factor += "~" + self.variables()[i]
                else:
                    factor += self.variables()[i]
            rv += factor + ")"
        
        variables = ""
        for i in self.variables():
            variables += i + ", "
        variables = variables[:-2]
        
        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._expression = ("f(%s) = %s" %(variables, rv))
        return rv2
                    
    def minimise(self):
        """
        Finds and returns the sum-of-products form of the Boolean Function 
        represented by the K-map.
        Uses Quine-McCluskey algorithm. 
        
        Source: http://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
        Runtime: O(exp(n)/n)

        ""
        It can be shown that for a function of n variables the upper bound on 
        the number of prime implicants is 3n/n. If n = 32 there may be over 
        6.5 * 10^15 prime implicants.
        "" 
        (Wikipedia)

        Better algorithms (e.g. ESPRESSO) are out of scope of this project, 
        given the time constraint. So this method is useful only for limited 
        number of variables.
        """

        pi = [] # Prime Implicants
        epi = [] # Essential Prime Implicants


        
        def next_pis(current_pi, level = 0):
            """
            Finds the next generation prime implicants from the current ones.

            current_pi is a dictionary mapping [num_ones, num_dashes] to a list
            of all the implicants in that category.
            """
            #if level == 0:
                
            next_list = []

            # Finding all the different categories of PIs
            categories = list(current_pi)
            categories.sort()

            # -1 because last category can't be processed
            for i in range(len(categories) - 1):

                category = categories[i]
                next_category = categories[i+1]

                for pi in current_pi[category]:
                    is_epi = False
                    # Checking for all PIs in current category
                    for high_pi in current_pi[next_category]:
                        # Comparing with all PIs in next category
                        if check_combine(pi, high_pi):
                            # If they differ by just 1 bit
                            next_list.append(combine_pis(pi, high_pi))
                            is_epi = False
                            # Merge them

                    if is_epi:
                        # If PI couldn't be combined, it is an EPI
                        next_list.append(pi)



def test_vals(minterms):
    """
    Tests if all the minterms (or dc) contain the same number of Boolean 
    variables.
    """
    base = len(minterms[0])

    for i in minterms:
        if len(i) != base: return False

    return True

def find_ones(n):
    """
    Given a number n, returns the number of 1's in its binary representation.
    """
    binary = bin(n)[2:]
    return sum([int(i) for i in binary])

def find_zeros(n, bits):
    """
    Given a number n, returns the number of 0's in its binary representation.
    Considers the "bits" number of bits
    """
    return (bits - find_ones(n))

def bin_conv(n, bits):
    """
    Given a number n, returns its binary representation in "bits" number of bits

    If "bits", can't completely contain all the bits, returns the lowest sig 
    bits.
    """
    rv = bin(n)[2:]
    if len(rv) >= bits: return rv[:bits]

    else:
        return "0"*(bits - len(rv)) + rv
