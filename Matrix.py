from functools import reduce

Num = (int, float, complex)

def toint(x):
    if isinstance(x, float) and int(x) == x:
        return int(x)
    elif isinstance(x, complex):
        return complex(toint(x.real), toint(x.imag))
    else:
        return x

def totup(x):
    if isinstance(x, Num):
        return (x,)
    elif isinstance(x, (list, tuple)) and reduce(lambda y, z: y and z, tuple(isinstance(i, Num) for i in x)):
        return tuple(x)
    else:
        raise ValueError("index should be number or tuple, list of numbers")

def zeros(m, n):
    return Matrix(tuple(tuple(0 for i in range(m)) for j in range(n)))

class Matrix(object):
    
    def __init__(self, Mtuple = ((0,),)):
        Unit = (Num, Matrix)
        def toMtx(x):
            if isinstance(x, Num):
                return Matrix(((x,),))
            elif isinstance(x, (tuple, list)):
                if min(isinstance(i, Unit) for i in x):
                    return Matrix((tuple(x),))
                else:
                    return Matrix(tuple(x))
                return Matrix(x.tup)
            else:
                return x
        if isinstance(Mtuple, Num):
            Mtuple = ((Mtuple,),)
        if len(Mtuple) == 1 and len(Mtuple[0]) == 1 and isinstance(Mtuple[0][0], Num):
            self.row = self.col = 1
            self.tup = ((toint(Mtuple[0][0]),),)
        else:
            p = list(filter(lambda x: len(x) == max(len(i) for i in Mtuple), Mtuple))[0]
            def fill(x):
                a = []
                for k in range(len(p)):
                    if k < len(x):
                        a.append(toMtx(x[k]))
                    else:
                        a.append(zeros(a[0].row, toMtx(p[k]).col))
                return tuple(a)
            Mtuple = tuple(map(fill, Mtuple))
            if min(reduce(lambda x, y: x + y, (tuple(j.row == Mtuple[i][0].row for j in Mtuple[i]) for i in range(len(Mtuple))))) and min(reduce(lambda x, y: x + y, (tuple(Mtuple[i][j].col == Mtuple[0][j].col for i in range(len(Mtuple))) for j in range(len(p))))):
                self.row = reduce(lambda x, y: x + y, (Mtuple[i][0].row for i in range(len(Mtuple))))
                self.col = reduce(lambda x, y: x + y, (Mtuple[0][j].col for j in range(len(p))))
                self.tup = reduce(lambda x, y: x + y, (tuple(reduce(lambda x, y: x + y, (Mtuple[i][j].tup[k] for j in range(len(p)))) for k in range(len(Mtuple[i][0].tup))) for i in range(len(Mtuple))))
            else:
                raise ValueError("unsupported partitioned matrix")
    
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
                return toint(x + y)
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
                return toint(x - y)
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
            return Matrix(tuple(tuple(toint(self[i][j]*other) for j in range(self.col)) for i in range(self.row)))
        if isinstance(other, Matrix):
            if self.col == other.row:
                return Matrix(tuple(tuple(toint(sum(self[i][k] * other.T()[j][k] for k in range(self.col))) for j in range(other.col)) for i in range(self.row)))
            else:
                raise ValueError("cannot multiply two matrices with unmatched column and row")
    
    __rmul__ = __mul__
    
    def __truediv__(self, num):
        if isinstance(num, Num):
            return self * (1/num)
        else:
            raise TypeError("unsupported operand type(s) for /") 
    
    def submatrix(self, idr, idc):
        return Matrix(tuple(tuple(self[i][j] for j in totup(idc)) for i in totup(idr)))
    
    def comsubmtx(self, idr, idc):
        return Matrix(tuple(tuple(self[i][j] for j in range(self.col) if j not in totup(idc)) for i in range(self.row) if i not in totup(idr)))
    
    @property
    def det(self):
        if self.row == self.col:
            if self.row == 1:
                return toint(self[0][0])
            else:
                return toint(sum(self[0][j] * self.comsubmtx(0, j).det * ((-1)**j) for j in range(self.col)))
        else:
            raise ValueError("only square matrices have determinants")
    
    def minor(self, idr, idc):
        return self.submatrix(idr, idc).det
    
    def cofactor(self, idr, idc):
        return self.comsubmtx(idr, idc).det * ((-1)**(sum(totup(idr))+sum(totup(idc))+len(totup(idr))+len(totup(idc))))
    
    def companion(self):
        if self.row == self.col:
            return Matrix(tuple(tuple(self.comsubmtx(i, j).det * ((-1)**(i+j)) for j in range(self.col)) for i in range(self.row))).T()
        else:
            raise ValueError("only square matrices have companions")
    
    def __pow__(self, num):
        if self.row == self.col:
            if isinstance(num, Num):
                if num == 1:
                    return self
                elif num == -1:
                    if self.det != 0:
                        return self.companion()/self.det
                    else:
                        raise ValueError("matrices with zero determinants do not have inverse matrix")
                else:
                    return self * (self ** (num - 1))   
            else:
                raise TypeError("unsupported operand type(s) for ** or pow()")
        else:
            raise ValueError("only square matrices can be powered")
    
    def inverse(self):
        return self**(-1)
    
    