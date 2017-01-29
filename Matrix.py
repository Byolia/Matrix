from functools import reduce

class Matrix(object):
    
    def __init__(self, Mtuple = ((0,),)):
        self.row = len(Mtuple)
        self.col = max(len(i) for i in Mtuple)
        def fill(x):
            a = []
            for i in range(self.col):
                if i < len(x):
                    a.append(x[i])
                else:
                    a.append(0)
            return tuple(a)
        self.tup = tuple(map(fill, Mtuple))
    
    def __str__(self):
        self.tup
        def Mstr(x):
            def Mdel(y):
                y.pop(0)
                return y
            if len(x) == 0:
                return ''
            else:
                return str(x[0]) + '\t' + Mstr(Mdel(x))
        return reduce(lambda x, y: x + '\n' + y, map(Mstr, map(list, self.tup)))
    
    __repr__ = __str__
    
    @property
    def len(self):
        return (self.row, self.col)
    
    def Row(self, n):
        return self.tup[n]
    
    def Col(self, n):
        return [self.tup[i][n] for i in range(len(self.tup))]
    
    def __getitem__(self, n):
        return self.tup[n]
    
    @property
    def T(self):
        return Matrix([self.Col(i) for i in range(self.col)])
    
    def __add__(self, other):
        def recadd(x, y):
            if isinstance(x, int) and isinstance(y, int):
                return x + y
            elif isinstance(x, tuple) and isinstance(y, tuple):
                return tuple(recadd(x[i], y[i]) for i in range(len(x)))
            elif isinstance(x, Matrix) and isinstance(y, Matrix):
                return tuple(recadd(x.tup[i], y.tup[i]) for i in range(len(x.tup)))
            else:
                raise TypeError("unsupported operand type(s) for +")
        return Matrix(recadd(self, other))
    
    __radd__ = __add__
    
    def __neg__(self):
        def recneg(x):
            if isinstance(x, int):
                return -x
            elif isinstance(x, tuple):
                return tuple(recneg(x[i]) for i in range(len(x)))
            else:
                raise TypeError("bad operand type for unary -")
        return Matrix(recneg(self))
    
    def __sub__(self, other):
        def recsub(x, y):
            if isinstance(x, int) and isinstance(y, int):
                return x - y
            elif isinstance(x, tuple) and isinstance(y, tuple):
                return tuple(recsub(x[i], y[i]) for i in range(len(x)))
            elif isinstance(x, Matrix) and isinstance(y, Matrix):
                return tuple(recsub(x.tup[i], y.tup[i]) for i in range(len(x.tup)))
            else:
                raise TypeError("unsupported operand type(s) for -")
        return Matrix(recsub(self, other))
    
    __rsub__ = __sub__
    
    def conjugate(self):
        return Matrix(tuple(tuple(self[i][j].conjugate() for j in range(self.col)) for i in range(self.row)))
    
    def 