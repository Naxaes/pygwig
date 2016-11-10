import sys


class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        try:
            return Vector2D(self.x * other, self.y * other)
        except TypeError as e:
            print(e, "\nUse @ for matrix multiplication", file=sys.stderr)
        raise TypeError

    def __truediv__(self, other):
        return Vector2D(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vector2D(self.x // other, self.y // other)

    def __matmul__(self, other):
        try:
            return self.x * other.x + self.y * other.y
        except TypeError as e:
            print(e, "\nUse * for scalar multiplication", file=sys.stderr)
        raise TypeError

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rfloordiv__ = __floordiv__
    __rmatmul__ = __matmul__

    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)

