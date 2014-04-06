"""
The Boolean Function module for the DigiCAD.
Runs the under-the-hood Boolean algebra required by it.
"""

from truth_tables import *
import copy, math, pdb

class InvalidBooleanFunctionError(Exception):
    pass

class BF:
    """
    Creates a boolean function 
    """

    def __init__(self, function, name = 'f'):

        # This name is useless if the function is in proper form
        # If not in proper form, this name will be applied
        function = proper(function, name)

        # After appropriate name is set up, store this name as an attribute
        self._name = find_name(function)

        # Parsing out the list of variables in the expression and creating the
        # truth table
        variables, table, symbols = make_table(function)
        
        minterms = [i for i in table if table[i]]
        maxterms = [i for i in table if not table[i]]

        # Store the vars, TT and the expression
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

    def _varstring(self):
            """
            Helper method that converts the list of variables to a string that 
            can be used in the outputs of any method that generates another 
            BF. 
            """
            variables = ""
            for i in self.variables():
                variables += i + ", "
            return variables[:-2]

    def truthtable(self):
        return copy.deepcopy(self._table)

    def name(self):
        return copy.deepcopy(self._name)

    def __str__(self):
        return copy.deepcopy(self._expression)

    def __repr__(self):
        return copy.deepcopy(self._expression)

    def __eq__(self, func):
        try:
            return self.truthtable() == func.truthtable()
        except AttributeError:
            raise InvalidBooleanFunctionError("Object isn't a Boolean Function!")

    def min_expand(self):
        """
        Returns the minterm expansion of the boolean function.
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
        
        if rv == "": rv = "0"

        variables = self._varstring()

        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._expression = ("%s_min_expand(%s) = %s" %(self.name(), variables, rv))
        return rv2        
                    
    def max_expand(self):
        """
        Returns the maxterm expansion form of the boolean function.
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
        
        if rv == "": rv = "1"
        variables = self._varstring()
        
        # Since it is the same Boolean function, all the attributes except the
        # expression are same. So just copy and return. Makes processing MUCH
        # faster
        rv2 = copy.deepcopy(self)
        rv2._expression = ("%s_max_expand(%s) = %s" %(self.name(), variables, rv))
        return rv2
    
    def sub(self, values):
        """
        Plus in the values in the BF and returns True/False. values in a string
        containing the values of the variables. (e.g. "1010")
        """        
        try:
            return self.truthtable()[values]
        except KeyError:
            raise KeyError("This value does not exist in the function's truth-table")
            
    def minimise(self):
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

        # PI contains all the different levels of PIs, such that pi[i] is the 2^i
        # level PI.
        
        pis_num = self.mintermsl() # Prime implicants, PIs = numerical minterms

        # Converting the minterms to a format appropriate for PIs
        pis = {}

        for i in pis_num:
            pis[i] = [] # Create empty minterm list for all categories 
            for j in pis_num[i]:
                string_minterm = bin_conv(j, int(math.log(len(self.truthtable()), 2)))
                pis[i].append(string_minterm)

        pis = [pis] # Converting to list to accomodate for future additions

        sim_pis = [] # Contains all the simplified prime implicants discovered so far

        i = 0
        comb_register = {}
        while(1):
            sim_pi_found, pis_calc, temp_register = next_pis(pis[i])

            # Because simplified PIs for current PIs are generated
            sim_pis += sim_pi_found

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

                        # Pop off the parent to remove duplicacy
                        #comb_register.pop(parent) 

            # Record the combination results
            comb_register.update(temp_register)

            if pis_calc == {i:[] for i in self.mintermsl()}:
                break # The most simplified version is created. So end
            else:
                pis.append(pis_calc)
                i += 1

        # Converting the string minterms to numeric minterms
        for i in comb_register:
            for j in range(len(comb_register[i])):
                comb_register[i][j] = int(comb_register[i][j], 2)

        # Generating EPIs from simplified PIs
        epis = gen_epi(self.minterms(), sim_pis, comb_register)
        
        # Generating Output
        variables = self._varstring()
        rv = form_function(epis, self.variables())
      
        rv2 = copy.deepcopy(self)
        rv2._expression = ("%s_simp(%s) = %s" %(self.name(), variables, rv))
        return rv2

        
def next_pis(current_pi):
    """
    Finds the next generation prime implicants from the current ones.

    current_pi is a dictionary mapping [num_ones, num_dashes] to a list
    of all the implicants in that category.
    If the PIs passed in are minterms, they are level 1 PIs. Function 
    will automatically convert them to the appropriate PI format.

    Test borrowed from Wikipedia's Quine-McCluskey algorithm page:
    
    >>> a = {1: ["0100", "1000"], 2: ["1001", "1010", "1100"], 3: ["1011", \
             "1110"], 4: ["1111"]}
    >>> sim_pis, npis, comb_register = next_pis(a)
    >>> sim_pis == []
    True
    >>> npis # Order may be opposite, but correct values tested 
    {1: ['100-', '-100', '1-00', '10-0'], 2: ['1-10', '11-0', '10-1', '101-'], 3: ['1-11', '111-'], 4: []}

    >>> comb_register
    {'-100': ['0100', '1100'],
     '1-00': ['1000', '1100'],
     '1-10': ['1010', '1110'],
     '1-11': ['1011', '1111'],
     '10-0': ['1000', '1010'],
     '10-1': ['1001', '1011'],
     '100-': ['1000', '1001'],
     '101-': ['1010', '1011'],
     '11-0': ['1100', '1110'],
     '111-': ['1110', '1111']}

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

    # -1 because last category can't be processed
    for i in range(len(categories) - 1):

        category = categories[i]
        next_category = categories[i+1]

        for pi in current_pi[category]:
            # Checking for all PIs in current category
            is_sim = True
            
            for high_pi in current_pi[next_category]:
                # Comparing with all PIs in next category

                combination = combine(pi, high_pi)
                if combination:
                    # If they differ by just 1 bit, then combination not = None
                    # Merge them
                    next_dict[category].append(combination)
                    is_sim = False
                    comb_register[combination] = [pi, high_pi]
                    # Adding the high_pi into list merged_pis as it is technically
                    # now merged. It is NOT the most simplified PI, even if no
                    # higher (higher than high) mergable PI is found.
                    merged_pis.append(high_pi)

            if is_sim and pi not in merged_pis:
                # If PI couldn't be combined, it is a simplified PI
                sim_pis.append(pi)

    # At this point, there will be duplicates of newly created PIs as different
    # combinations can lead to the same mere.

    for i in next_dict:
        next_dict[i] = list(set(next_dict[i]))
        
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

    # Finding minterms that are formed by just 1 sim_pi
    pi_tally = {i:[] for i in minterms}

    # Keeps track of which minterms are already covered by the contents of EPI
    minterms_covered = []

    for pi in sim_pis:
        # Loop over all the simplified PIs
        for minterm in comb_register[pi]:
            # Run over all the minterms that were combined to get this PI
            pi_tally[minterm].append(pi)
            # Add this PI to that minterm's PI-tally

    for minterm in pi_tally:
        if len(pi_tally[minterm]) == 1:
            # This minterm can be formed only by 1 PI
            # This PI is EPI
            EPI.append(pi_tally[minterm][0])

            # Pulling out all the minterms that can be covered by this EPI
            # Putting them in the list of minterms covered
            minterms_covered += comb_register[pi_tally[minterm][0]]

    # Work left
    minterms_left = [i for i in minterms if i not in minterms_covered]

    while minterms_left:
        
        minterm = minterms_left.pop()

        possible_choices = pi_tally[minterm]
        choice = max(possible_choices, key = lambda x: len(comb_register[x]))

        EPI.append(choice)
        # The choice PI will have some other minterms that it covers, which might
        # be there in the list of minterms_left. Pop them off

        for i in comb_register[choice]:
            if i in minterms_left: minterms_left.remove(i)


    return EPI

def form_function(epis, vars):
    """
    Given a list of epis and the desired vars (same order), returns a 
    string that can be used for forming a BF.
    
    This function assumes that epis actually contain epis! It does not do any
    simplification. Can produce unexpected results if called that way.

    This will also simiplify using the identity:
    a + a = a

    The similar simiplification using a*a = a is not done! Other parts of who 
    call this should do it!

    >>> form_function(['001', '-1-'], ['a', 'b', 'c'])
    '~a*~b*c + b'

    >>> form_function(['---'], ['a','b','c'])
    '1'
    """

    # This removes repetitive EPIs which might have lingered on.
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
                    # Term needs a negated form of this variable
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
        # All the variables have a "-". It is the always true function
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
    """
    rv = 0
    for i in pi:
        if i == "1": rv += 1

    return rv