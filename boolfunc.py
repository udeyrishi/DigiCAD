"""
The Boolean Function (BF) module.
Provides tools to store and manipulate BFs. 

Please note that some of the test cases in this module may fail. The exact test
result depends on how Python interpreter decides to store dictionaries. In case
test(s) fails, check the 'expected' vs. 'got' values to verify manually.

Developed by: Udey Rishi, 2014
"""

from truth_tables import *
import copy, math

class InvalidBooleanFunctionError(Exception):
    """
    Handles the exceptions conncerning Invalid BFs.
    """
    pass

class BF:
    """
    The BF class. Stores the details of a BF and provides numerous methods to do
    computations on them. 

    Can take the BF in 3 ways:
    1. Expression: e.g. BF("a+b")
    2. Partial Proper: e.g. BF("f = a+b"), or BF("a+b", "f")
    3. Proper: e.g. BF("f(a,b) = a+b")

    The BF needs a name assigned to it in multiple use cases; the proper and partial
    proper ways ensure that the user assigned name is assigned to the BF. In the
    case where just the expression is passed in, a default name "f" is assigned.
    The proper way is more specific than partial proper, as it also specifies
    the variables that user intended; any contradiction will lead to error. 
    But this of course, is optional. The parsing engine has the capability to 
    recognise the variables, which is pretty accurate in its prediction in mose
    scenarios.

    The spaces will be adjusted properly. This module uses the truth-table 
    generating engine (truth_tables.py), which relies on its own parsing engine.
    As a general rule, brackets are given the highest priority. For other priority
    details, see strings.py.   
    """

    def __init__(self, function, name = 'f'):

        # Converts the function to its proper version using the best estimation
        function = proper(function, name)

        # After appropriate name is set up, store this name as an attribute
        self._name = find_name(function)

        # Parsing out the list of variables and expression, and creating the
        # truth table (tt) from the proper function
        variables, table, expression = make_table(function)

        variables.sort()

        # Reading out the minterms and maxterms from the tt
        minterms = [i for i in table if table[i]]
        maxterms = [i for i in table if not table[i]]

        # Store the vars, TT, and the expression as attributes of the BF
        self._expression = expression
        self._variables = variables
        self._table = table

        # If a single variable is given, e.g. BF('x = x'), turn it to 'f = x'
        if self._expression.strip() == self._name.strip():
            self._name = name
        # Storing minterms hashed with the number of 1s, and maxterms hashed 
        # with the number of 0s
        # This is done as minterms and maxterms are needed in a majority of
        # computations, and storing them will save time

        # The minterms/maxterm are in the form of bit-strings. Convert them into 
        # their numerical versions for storing for performing Boolean computations
        self._minterms = {}

        minterms2 = list()
        
        # Converting the string buts into numerical bit lists
        for i in minterms:
            minterms2.append(int(i, 2))

        for i in minterms2:
            if find_ones(i) in self._minterms:
                self._minterms[find_ones(i)].append(i)
            else:
                self._minterms[find_ones(i)] = [i]

        # Do the same for the maxterms, just hashed with # of zeroes instead
        self._maxterms = {}

        maxterms2 = list()

        for i in maxterms:
            maxterms2.append(int(i, 2))

        for i in maxterms2:
            if find_zeros(i, len(variables)) in self._maxterms:
                self._maxterms[find_zeros(i, len(variables))].append(i)
            else:
                self._maxterms[find_zeros(i, len(variables))] = [i]


        # Storing simplified expressions as a cache. This will be filled the
        # first time the appropriate methods are called
        self._min_exp = None
        self._max_exp = None
        self._min_sop = None
        self._min_pos = None

    def expression(self):
        """
        Returns the BF expression. 
        """
        return self._expression

    def minterms(self):
        """
        Returns a sorted list of the minterms.
        """
        rv = []
        for i in self._minterms.values():
            rv += i 
        rv.sort()
        return copy.deepcopy(rv) # Lists are mutable

    def mintermsl(self):
        """
        Returns a long version of the minterms, mapping the # of 1's in it to
        the actual minterm.
        """
        return copy.deepcopy(self._minterms) # Dicts are mutable

    def maxterms(self):
        """
        Returns a sorted list of the maxterms.
        """
        rv = []
        for i in self._maxterms.values():
            rv += i 
        rv.sort()
        return copy.deepcopy(rv) # Lists are mutable

    def maxtermsl(self):
        """
        Returns a long version of the maxterms, mapping the # of 0's in it to
        the actual minterm.
        """ 
        return copy.deepcopy(self._maxterms) # Dicts are mutable

    def variables(self):
        """
        Returns a copy of the variables in the BF.
        """
        return copy.deepcopy(self._variables) # Lists are mutable

    def _varstring(self):
        """
        Helper method that converts the list of variables to a string.  
        Can be used in the outputs of methods that needs to generate another 
        BF. 
        """
        variables = ""
        for i in self.variables():
            variables += i + ", "
        return variables[:-2] # Remove the extra ", " at the end

    def truthtable(self):
        """
        Returns the BF's tt.
        """
        return copy.deepcopy(self._table)

    def name(self):
        """
        Returns the name of the BF.
        """
        return copy.deepcopy(self._name)

    def _print(self):
        """
        Returns a string representing the entire BF in the proper form. 
        Helper method for other methods.
        NOT the same as just calling the BF instance, as that returns another BF
        object, not a string. 
        """
        return ("%s(%s) = %s" %(self._name, self._varstring(), self.expression()))       

    # The following two are just used for making object interaction user firendly
    def __str__(self):
        return ("%s(%s) = %s" %(self._name, self._varstring(), self.expression()))

    def __repr__(self):
        return ("%s(%s) = %s" %(self._name, self._varstring(), self.expression()))

    
    def __eq__(self, func):
        """
        Equates the 2 BFs
        """
        try:
            return self.truthtable() == func.truthtable()
        except AttributeError:
            raise InvalidBooleanFunctionError("Object isn't a Boolean Function!")

    
    # Operators to combine boolean functions:
    
    def __add__(self, other):
        """
        Finds the OR of the BFs
        """
        try:
            return BF("(%s) + (%s)" %(self.expression(), other.expression()), \
                      "%s_OR_%s" %(self.name(), other.name()))

        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")

    def __radd__(self, other):
        """
        Finds the OR of the BFs
        """
        try:
            return BF("(%s) + (%s)" %(other.expression(), self.expression()), \
                      "%s_OR_%s" %(other.name(), self.name()))
            
        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")
        

    def __mul__(self, other):
        """
        Finds the AND of the BFs
        """
        try:
            return BF("(%s) * (%s)" %(self.expression(), other.expression()), \
                      "%s_AND_%s" %(self.name(), other.name()))

        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")


    
    def __rmul__(self, other):
        """
        Finds the AND of the BFs
        """
        try:
            return BF("(%s) * (%s)" %(other.expression(), self.expression()), \
                      "%s_AND_%s" %(other.name(), self.name()))
            
        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")
        

    def __xor__(self, other):
        """
        Finds the XOR of the BFs
        """
        try:
            return BF("(%s) % (%s)" %(self.expression(), other.expression()), \
                      "%s_XOR_%s" %(self.name(), other.name()))
            
        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")
        
    def __rxor__(self, other):
        """
        Finds the XOR of the BFs
        """
        try:
            return BF("(%s) % (%s)" %(other.expression(), self.expression()), \
                      "%s_XOR_%s" %(other.name(), self.name()))
            
        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")

    def bf_not(self):
        """
        Returns a not version of the boolean function.
        """
        try:
            string = ("~(%s)" %(self.expression()))
            return BF(string, ("%s_NOT" %self.name()))
        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")

    def nor(self, other):
        """
        Returns a NOR-ed version of self with the boolean function passed in.
        """     
        try:
            string = ("(%s) - (%s)" %(self.expression(), other.expression()))
            return BF(string, ("%s_NOR_%s" %(self.name(), other.name())))

        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")

    def nand(self, other):
        """
        Returns a NAND-ed version of self with the boolean function passed in.
        """     
        try:
            string = ("(%s) | (%s)" %(self.expression(), other.expression()))
            return BF(string, ("%s_NAND_%s" %(self.name(), other.name())))

        except AttributeError:
            raise InvalidBooleanFunctionError("The object is not a Boolean Function")

    def min_expand(self):
        """
        Returns the minterm expansion of the boolean function.
        """
        if self._min_exp:
            # Checking of there is a cached value
            rv = self._min_exp

        else: 
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
                        # It should be a non-complemented variable
                        term += self.variables()[i]
                    else:
                        # It should be a complemented variable
                        term += "~" + self.variables()[i]
                rv += term
            
            if rv == "": rv = "0" # Special case: no minterms

            self._min_exp = rv # Cache the calculated expression
        variables = self._varstring()

        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._name = "%s_min_expand" %self.name()
        rv2._expression = "%s" %rv
        return rv2
                    
    def max_expand(self):
        """
        Returns the maxterm expansion form of the boolean function.
        """
        
        if self._max_exp:
            # Checking of there is a cached value
            rv = self._max_exp

        else:
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
                        # Variable should be complemented
                        factor += "~" + self.variables()[i]
                    else:
                        # Variable should be in original form
                        factor += self.variables()[i]
                rv += factor + ")"
            
            if rv == "": rv = "1" # Special case: No maxterms

            self._max_exp = rv # Caching the calculated value
        variables = self._varstring()
        
        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._name = "%s_max_expand" %self.name()
        rv2._expression = "%s" %rv
        return rv2
    
    def sub(self, values):
        """
        Plugs in the values in the BF and returns True/False. values is a string
        containing the values of the variables in a sorted order. (e.g. "1010")
        """        
        try:
            return self.truthtable()[values]
        except KeyError:
            raise KeyError("This value does not exist in the function's truth-table")
            
    def min_sop(self):
        """
        Finds and returns the simplified sum-of-products form of the Boolean
        Function.
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

        if self._min_sop:
            # Retrieving from cache
            rv = self._min_sop

        
        else:
            # 2 Extreme cases for faster computations
            if len(self.minterms()) == 0: 
                # There are no minterms
                rv = '0'
            
            elif len(self.maxterms()) == 0:
                # All the values in truthtable are minterms
                rv = "1"

            # General case
            else:
                # STAGE 1 OF Q-M ALGORITHM

                # First level PIs are the minterms themselves
                pis_num = self.mintermsl()

                # Register storing all the combinations. Used for tracing back
                # the minterms covered
                comb_register = {}

                # Converting the minterms (PIs) from numerical to string format
                # for analysing bit by bit. 
                # Numerical versions are still needed for checking if all the 
                # required minterms are covered later...so a new copy
                pis = {}
                for i in pis_num:
                    pis[i] = [] # Create empty minterm list for all categories 
                    for j in pis_num[i]:
                        string_minterm = bin_conv(j, int(math.log(len(self.truthtable()), 2)))
                        pis[i].append(string_minterm)
                        # Populating the cover sheet comb register
                        comb_register[string_minterm] = [string_minterm] 

                # pis contains all the different levels of PIs, such that pis[i] 
                # is the 2^i level PI.
                # Converting to list to accomodate for future additions
                pis = [pis]

                # Contains all the simplified prime implicants discovered so far
                sim_pis = []

                # Doing the repetitive prime impliciation simplification
                i = 0
                while(1):
                    # Find the new PIs calculated, the simplified PIs found
                    # in the current PIs, and the temporary combination register
                    # developed during this simplification
                    sim_pi_found, pis_calc, temp_register = next_pis(pis[i])

                    # These are the required simplified PIs
                    sim_pis += sim_pi_found

                    # Finding out the minterms involved in the merge
                    for merge in temp_register:
                        # For all the merged results

                        parents = copy.deepcopy(temp_register[merge])

                        for parent in parents:
                            if parent in comb_register:
                                # Checking if parents of merge were themselves merged earlier
                                grandparents = comb_register[parent]
                                # Substitute the parents with grandparents to get the minterms
                                temp_register[merge] += grandparents
                                temp_register[merge].remove(parent)

                    # Record the combination results
                    comb_register.update(temp_register)

                    if pis_calc == {i:[] for i in self.mintermsl()}:
                        break # The most simplified version is created. So end
                    else:
                        pis.append(pis_calc)
                        i += 1

                # STAGE 2 OF Q-M ALGORITHM

                # Converting the string minterms to numeric minterms
                for i in comb_register:
                    for j in range(len(comb_register[i])):
                        comb_register[i][j] = int(comb_register[i][j], 2)

                # Generating EPIs from simplified PIs == PI chart
                epis = gen_epi(self.minterms(), sim_pis, comb_register)
                
                # Generating Output
                variables = self._varstring()
                rv = form_function(epis, self.variables())
                
                self._min_sop = rv # Caching the calculated value

        rv2 = copy.deepcopy(self)
        rv2._name = ("%s_min_sop" %self.name())
        rv2._expression = rv
        return rv2

    def min_pos(self):
        """
        Finds and returns the most simplified POS form of the boolean function.
        """

        # This should be able to be implemented by finding adapting the Q-M
        # algorithm for POS. Couldn't implement due to lack of time
        print("Still under development. Try min_sop instead")
        
def next_pis(current_pi):
    """
    Finds the next generation prime implicants from the current ones.

    current_pi is a dictionary mapping num_ones to a list of all the implicants 
    in that category.
    
    Test borrowed from Wikipedia's Quine-McCluskey algorithm page:
    
    >>> a = {1: ["0100", "1000"], 2: ["1001", "1010", "1100"], 3: ["1011", \
             "1110"], 4: ["1111"]}
    >>> sim_pis, npis, comb_register = next_pis(a)
    >>> sim_pis == []
    True
    >>> npis # Order may be opposite, but correct values tested 
    {1: ['100-', '-100', '1-00', '10-0'], 2: ['11-0', '10-1', '1-10', '101-'], 3: ['1-11', '111-'], 4: []}

    >>> comb_register == {'-100': ['0100', '1100'], \
                          '1-00': ['1000', '1100'], \
                          '1-10': ['1010', '1110'], \
                          '1-11': ['1011', '1111'], \
                          '10-0': ['1000', '1010'], \
                          '10-1': ['1001', '1011'], \
                          '100-': ['1000', '1001'], \
                          '101-': ['1010', '1011'], \
                          '11-0': ['1100', '1110'], \
                          '111-': ['1110', '1111']}
    True

    >>> sim_pis2, npis2, comb_register2 = next_pis(npis)
    >>> sim_pis2
    ['-100']
    >>> npis2 # Order may be opposite, but correct values tested
    {1: ['10--', '1--0'], 2: ['1-1-'], 3: [], 4: []}

    >>> comb_register2
    {'1--0': ['10-0', '11-0'], '1-1-': ['1-10', '1-11'], '10--': ['10-0', '10-1']}
    """
    
    # Contains the list of PIs formed after simplifying current stage
    next_dict =  {}

    # Creating the categories in the next_dict
    for i in current_pi:
        next_dict[i] = list()

    # Contains the list of PIs from current stage that are already simplified
    sim_pis = []

    # Stores all the PIs that have been merged to form next_dict
    merged_pis = []

    # Stores how the merged PI was formed (combining which previous PIs)
    comb_register = {}

    # Extracting all the categories of PIs (based on # of ones)
    categories = list(current_pi)
    categories.sort()

    for i in range(len(categories)):
        category = categories[i]
        if i+1 < len(categories):
            # We haven't reached the last category
            next_category = categories[i+1]
        else: 
            # Last category, so no comparison to a non-existent next-category
            next_category = None

        for pi in current_pi[category]:
            # Checking for all PIs in current category
            
            if next_category:
                # Only try to merge if the next category exists
                for high_pi in current_pi[next_category]:
                    # Comparing with all PIs in next category

                    combination = combine(pi, high_pi)
                    if combination:
                        # Record the merged result
                        next_dict[category].append(combination)
                        comb_register[combination] = [pi, high_pi]
                        # Adding the 2 PIs to the list of merged PIs
                        merged_pis.append(high_pi)
                        merged_pis.append(pi)

            if pi not in merged_pis:
                # This is the most simplified PI
                sim_pis.append(pi)

    # The same resulting PI can be generated by multiple combinations. So there
    # will be duplicates. # of duplicates is alays 2^i for some i

    for i in next_dict:
        next_dict[i] = list(set(next_dict[i])) # Removes the duplicates
        
    return sim_pis, next_dict, comb_register

def combine(pi1, pi2):
    """
    Combines pi1 and pi2 to return the combined pi. Returns None if they can't 
    be combined.

    Make sure that the 2 pis are of the same length.

    >>> combine("0000", "1111")
    >>> combine("0001", "1001")
    '-001'
    >>> combine('10--', '00--')
    '-0--'
    >>> combine('1--1', '1--0')
    '1---'
    """
    
    diff_list = [] # Keeps track of whick indices in the bit string are different

    for i in range(len(pi1)):
        if pi1[i] != pi2[i]:
            diff_list.append(i)

    if len(diff_list) == 1:
        # The PIs can be combined
        return pi1[:diff_list[0]] + '-' + pi1[diff_list[0] + 1:]

    else:
        # The PIs can't be combined if more than 1 bit are different
        return None

    # 0 bit difference == identical PIs (can never happen in the first place)


def gen_epi(minterms, sim_pis, comb_register):
    """
    Given a list of prime implicants that can't be simplified further, finds and
    returns a list of essential PIs. Based on the step 2 (prime implication chart)
    of Quine-McCluskey algorithm. 

    comb_register stores which minterms were combined to eventually form the 
    sim_pis.

    Test copied from Quine-McCluskey algorithm's Wikipedia page:

    >>> minterms = [4,8,9,10,11,12,14,15]

    >>> sim_pis = ["-100", "10--", "1--0", "1-1-"]

    >>> comb_register = {"-100" : [4,12], "10--":[8,9,10,11], "1--0" :[8,10,12,14], "1-1-":[10, 11, 14, 15]}

    >>> gen_epi(minterms, sim_pis, comb_register)
    ['-100', '10--', '1-1-']

    """
    EPI = []

    if sim_pis and comb_register == {}:
        # Extreme case where no merges happened, but there are PIs in sim_pis
        # These sim_pis are the EPIs
        EPI = sim_pis        

    else:
        # Finding minterms that are formed by just 1 sim_pi
        pi_tally = {i:[] for i in minterms}

        # Keeps track of which minterms are already covered by the contents of EPI
        minterms_covered = []

        for pi in sim_pis:
            # Loop over all the simplified PIs
            for minterm in comb_register[pi]:
                # Loop over all the minterms that were combined to get this PI
                pi_tally[minterm].append(pi)
                # Add this PI to that minterm's PI-tally

        for minterm in pi_tally:
            # Now analysing all the minterms for their coverage by PIs
            if len(pi_tally[minterm]) == 1:
                # This minterm can be formed only by 1 PI
                # This PI is an EPI
                EPI.append(pi_tally[minterm][0])

                # Pulling out all the minterms that can be covered by this EPI
                # Putting them in the list of minterms covered as well
                minterms_covered += comb_register[pi_tally[minterm][0]]

        # Work left
        minterms_left = [i for i in minterms if i not in minterms_covered]

        while minterms_left:
            # Choosing EPIs based on the number of minterms they cover.
            # This should produce the accurate results in most cases, and it 
            # tries to simulate the trial and error technique used in reality.
            # Nevertheless, a more thorough testing is needed.

            # Petrick's Method can be implemented in an improved version
            # http://en.wikipedia.org/wiki/Petrick%27s_method
            minterm = minterms_left.pop()
            possible_choices = pi_tally[minterm]
            choice = max(possible_choices, key = lambda x: len(comb_register[x]))

            EPI.append(choice)
            # The choice PI will have some other minterms that it covers, which 
            # might be there in the list of minterms_left. Pop them off

            for i in comb_register[choice]:
                if i in minterms_left: minterms_left.remove(i)

    return EPI

def form_function(epis, vars):
    """
    Given a list of epis and the desired vars (same order), returns a 
    string that can be used for forming a BF.
    
    This function assumes that epis actually contain epis! Can produce 
    unexpected results if called in any other case.

    This will also simplify using the identity:
    a + a = a

    The similar simiplification using a*a = a is not done! Other parts of who 
    call this should do it!

    >>> form_function(['001', '-1-'], ['a', 'b', 'c'])
    '~a*~b*c + b'

    >>> form_function(['---'], ['a','b','c'])
    '1'
    """

    # This removes repetitive EPIs which might have lingered on. Applies the
    # "a + a = a" identity
    epis = list(set(epis))

    epis.sort(key = find_ones_pi)
    rv = ""
    for epi in epis:
        # Going over all the EPIs

        term = ""
        for i in range(len(vars)):
            # Parsing this EPI bit by bit
                if epi[i] == "0":
                    # Term needs a negated form of this variable
                    if term != "":
                        term += "*~" + vars[i]
                    else:
                        term += "~" + vars[i]

                elif epi[i] == "1":
                    # Term needs a non-negated form of this variable
                    if term != "":
                        term += "*" + vars[i]
                    else:
                        term += vars[i]

                # Else, this bit can be "-", meaning variable is not needed. Skip

        if rv != "":
            rv += " + " + term
        else:
            rv += term

    if rv == "":
        # All the variables have a "-". It is the identity 1
        return "1"
    else:
        return rv


def find_ones(n):
    """
    Given a number n, returns the number of 1's in its binary representation.

    >>> find_ones(10)
    2
    >>> find_ones(7)
    3
    """
    binary = bin(n)[2:]
    return sum([int(i) for i in binary])

def find_zeros(n, bits):
    """
    Given a number n, returns the number of 0's in its binary representation.
    Considers the "bits" number of bits
    
    >>> find_zeros(7, 4)
    1
    >>> find_zeros(7, 3)
    0
    """
    return (bits - find_ones(n))

def bin_conv(n, bits):
    """
    Given a number n, returns its binary representation in "bits" number of bits

    If "bits", can't completely contain all the bits, returns the lowest sig 
    bits.

    >>> bin_conv(10, 5)
    '01010'
    >>> bin_conv(7, 2)
    '11'
    >>> bin_conv(7,3)
    '111'
    """
    rv = bin(n)[2:]
    if len(rv) >= bits: return rv[:bits]

    else:
        return "0"*(bits - len(rv)) + rv

def find_ones_pi(pi):
    """
    Given a PI (in its standard format), returns the number of 1's contained in 
    it.

    >>> find_ones_pi('10101')
    3
    >>> find_ones_pi('11')
    2
    >>> find_ones_pi('10--1')
    2
    """
    rv = 0
    for i in pi:
        if i == "1": rv += 1

    return rv


# Copying the methods as functions to make the module more user friendly
def bf_not(bf):
    """
    Returns a not version of the boolean function passed in.
    """
    return bf.bf_not()

def nor(bf1, bf2):
    """
    Returns a NOR-ed version of the boolean functions passed in.
    """     
    return bf1.nor(bf2)

def nand(bf1, bf2):
    """
    Returns a NAND-ed version of the boolean functions passed in.
    """     
    return bf1.nand(bf2)

def equal(bf1, bf2):
    """
    Checks if the two BFs are equivalent
    """
    return bf1 == bf2
    
def bf_or(bf1, bf2):
    """
    Does the boolean OR operation and returns the resulting function (without 
    simplifying)
    """
    return bf1 + bf2

def bf_and(bf1, bf2):
    """
    Does the boolean AND operation and returns the resulting function (without 
    simplifying)
    """
    return bf1*bf2
    
def xor(bf1, bf2):
    """
    Does the boolean XOR operation and returns the resulting function (without 
    simplifying)
    """
    return bf1%bf2


a = BF("x")