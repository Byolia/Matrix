from functools import reduce

Num = (int, float, complex)

def totup(x):
    if isinstance(x, Num):
        return (x,)
    elif isinstance(x, (list, tuple)) and reduce(lambda y, z: y and z, tuple(isinstance(i, Num) for i in x)):
        return tuple(x)
    else:
        raise ValueError("index should be number or tuple, list of numbers")

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
    
    def T(self):
        return Matrix([self.Col(i) for i in range(self.col)])
    
    def __add__(self, other):
        def recadd(x, y):
            if isinstance(x, Num) and isinstance(y, Num):
                return x + y
            elif isinstance(x, tuple) and isinstance(y, tuple):
                return tuple(recadd(x[i], y[i]) for i in range(len(x)))
            elif isinstance(x, Matrix) and isinstance(y, Matrix):
                if x.row == y.row and x.col == y.col:
                    return tuple(recadd(x.tup[i], y.tup[i]) for i in range(len(x.tup)))
                else:
                    raise ValueError("cannot add two matrices with unmatched column and row")
            else:
                raise TypeError("unsupported operand type(s) for +")
        return Matrix(recadd(self, other))
    
    __radd__ = __add__
    
    def __neg__(self):
        def recneg(x):
            if isinstance(x, Num):
                return -x
            elif isinstance(x, tuple):
                return tuple(recneg(x[i]) for i in range(len(x)))
            else:
                raise TypeError("bad operand type for unary -")
        return Matrix(recneg(self))
    
    def __sub__(self, other):
        def recsub(x, y):
            if isinstance(x, Num) and isinstance(y, Num):
                return x - y
            elif isinstance(x, tuple) and isinstance(y, tuple):
                return tuple(recsub(x[i], y[i]) for i in range(len(x)))
            elif isinstance(x, Matrix) and isinstance(y, Matrix):
                if x.row == y.row and x.col == y.col:
                    return tuple(recsub(x.tup[i], y.tup[i]) for i in range(len(x.tup)))
                else:
                    raise ValueError("cannot subtract two matrices with unmatched column and row")
            else:
                raise TypeError("unsupported operand type(s) for -")
        return Matrix(recsub(self, other))
    
    __rsub__ = __sub__
    
    def conjugate(self):
        return Matrix(tuple(tuple(self[i][j].conjugate() for j in range(self.col)) for i in range(self.row)))
    
    def __mul__(self, other):
        if isinstance(other, Num):
            return Matrix(tuple(tuple(self[i][j]*other for j in range(self.col)) for i in range(self.row)))
        if isinstance(other, Matrix):
            if self.col == other.row:
                return Matrix(tuple(tuple(sum(self[i][k] * other.T()[j][k] for k in range(self.col)) for j in range(other.col)) for i in range(self.row)))
            else:
                raise ValueError("cannot multiply two matrices with unmatched column and row")
    
    __rmul__ = __mul__
    
    def __truediv__(self, num):
        if isinstance(num, Num):
            return self * (1/num)
        else:
            raise TypeError("unsupported operand type(s) for *") 
    
    def minor(self, idr, idc):
        return Matrix(tuple(tuple(self[i][j] for j in totup(idc)) for i in totup(idr)))
    
    def cofactor(self, idr, idc):
        return Matrix(tuple(tuple(self[i][j] for j in range(self.col) if j not in totup(idc)) for i in range(self.row) if i not in totup(idr)))
    
    @property
    def det(self):
        if self.row == self.col:
            if self.row == 1:
                return self[0][0]
            else:
                return sum(self[0][j] * self.cofactor(0, j).det * ((-1)**j) for j in range(self.col))
        else:
            raise ValueError("only square matrices have determinants")
    
    def companion(self):
        if self.row == self.col:
            return Matrix(tuple(tuple(self.cofactor(i, j).det * ((-1)**(i+j)) for j in range(self.col)) for i in range(self.row))).T()
        else:
            raise ValueError("only square matrices have companions")
    
    def __pow__(self, num):
        if self.row == self.col:
            if isinstance(num, Num):
                if num == 1:
                    return self
                if num == -1:
                    return self.companion()*(1/self.det)
                else:
                    return self * (self ** (num - 1))   
            else:
                raise TypeError("unsupported operand type(s) for ** or pow()")
        else:
            raise ValueError("only square matrices can be powered")