from typing import Self

class Vector2:
    
    def orthogonal():
        yield Vector2( 0, -1)
        yield Vector2( 1,  0)
        yield Vector2( 0,  1)
        yield Vector2(-1,  0)

    def __init__(self: Self, x, y) -> None:
        self.x = x
        self.y = y

    def __copy__(self: Self) -> Self:
        return Vector2(self.x, self.y)

    def __eq__(self: Self, other: Self):
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y
    
    def __lt__(self: Self, other: Self):
        return self.x < other.x or self.x == other.x and self.y < other.y

    def rotate_clockwise(self: Self) -> None:
        self.x, self.y = -self.y, self.x

    def rotate_counter_clockwise(self: Self) -> None:
        self.x, self.y = self.y, -self.x

    def __add__(self: Self, v: Self) -> Self:
        return Vector2(self.x + v.x, self.y + v.y)
    
    def __sub__(self: Self, v: Self) -> Self:
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self: Self, s: Self) -> Self:
        return Vector2(self.x * s, self.y * s)
    
    def __rmul__(self: Self, s: Self) -> Self:
        return self.__mul__(s)

    def __neg__(self: Self) -> Self:
        return self * -1

    def __repr__(self: Self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self: Self) -> str:
        return hash(repr(self))

    def __iter__(self: Self):
        yield self.x
        yield self.y