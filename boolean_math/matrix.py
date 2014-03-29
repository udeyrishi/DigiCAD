class InvalidMatrixError(Exception):
    pass

class Matrix:
    """
    n-D matrix class.
    Divides the matrix into sub-dimensions by using paranthesis.

    >>> a = Matrix(((1,2,3), (3,4,5)), 2)
    >>> a
    [[1, 2, 3], [3, 4, 5]]
    >>> a[0,0]
    1
    >>> a[1,0]
    3
    # The following is an e.g. of a 3-D matrix
    >>> a = Matrix( (((0,2,3), (43,4,5)) , ((6,5,2), (8,1,3))), 3) 
    >>> a[1,1,1]
    1
    """
    
    def __init__(self, *args):
        # Checking if values match the matrix syntax
        if len(args) !== 2:
            raise InvalidMatrixError("Data entered does not correspond to a matrix")

        num_dim = args[1]
        data = args[0]

        for i in data:
            
            
        # Creating Matrix                                          
        self._rows = [list(i) for i in rows]

    def __getitem__(self, ij):
        i, j = ij
        return self._rows[i][j]
   
    def __str__(self): 
        return list(self._rows)
        
    def __repr__(self):
        return str(list(self._rows))
        
    def update(self, i, j, new_value):
        self._rows[i][j] = new_value
    
    def row(self, i):
        return list(self._rows[i])
    
    def column(self, j):
        return [i[j] for i in self._rows]
        
    def sum(self):
        rv = 0
        for i in self._rows:
            for j in i:
                rv += j
        return rv
        
    def abs_sum(self):
        rv = 0
        for i in self._rows:
            for j in i:
                rv += abs(j)
        return rv
    
    def sum_row(self, i):
        return sum(j for j in self.row(i))
    
    def sum_column(self, j):
        return sum(i for i in self.column(j))
    
    def swap_sign_row(self, i):
        self._rows[i] = [-j for j in self._rows[i]]
    
    def swap_sign_col(self,j):
        for i in self._rows:
            i[j] = -i[j]
    
