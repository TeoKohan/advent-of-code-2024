from typing import Self

class Vector2:
    
    def taxicab_distance(u: Self, v: Self) -> int:
        return abs(u.x - v.x) + abs(u.y - v.y)

    def zero() -> Self:
        return Vector2( 0,  0)
    def one() -> Self:
        return Vector2( 1,  1)
    def up() -> Self:
        return Vector2(-1,  0)
    def right() -> Self:
        return Vector2( 0,  1)
    def down() -> Self:
        return Vector2( 1,  0)
    def left() -> Self:
        return Vector2( 0, -1)
    
    def orthogonal():
        yield Vector2( 0, -1)
        yield Vector2( 1,  0)
        yield Vector2( 0,  1)
        yield Vector2(-1,  0)

    def __init__(self: Self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    def __copy__(self: Self) -> Self:
        return Vector2(self.x, self.y)

    def __eq__(self: Self, other: Self):
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y
    
    def __lt__(self: Self, other: Self):
        return self.x < other.x or self.x == other.x and self.y < other.y

    def rotate_clockwise(self: Self) -> None:
        self.x, self.y = -self.y, self.x

    def rotated_clockwise(self: Self) -> Self:
        return Vector2(-self.y, self.x)

    def rotate_counter_clockwise(self: Self) -> None:
        self.x, self.y = self.y, -self.x
    
    def rotated_counter_clockwise(self: Self) -> Self:
        return Vector2(self.y, -self.x)
    
    def x_project(self: Self) -> Self:
        return Vector2(self.x, 0)
    
    def y_project(self: Self) -> Self:
        return Vector2(0, self.y)

    def __add__(self: Self, v: Self) -> Self:
        return Vector2(self.x + v.x, self.y + v.y)
    
    def __iadd__(self: Self, v: Self):
        self.x += v.x
        self.y += v.y
        return self
    
    def __sub__(self: Self, v: Self) -> Self:
        return Vector2(self.x - v.x, self.y - v.y)

    def __isub__(self: Self, v: Self) -> Self:
        self.x -= v.x
        self.y -= v.y
        return self

    def __mul__(self: Self, s: int | Self) -> Self:
        if isinstance(s, int):
            return Vector2(self.x * s, self.y * s)
        if isinstance(s, Vector2):
            return Vector2(self.x * s.x, self.y * s.y)
        else:
            raise TypeError()
    
    __rmul__ = __mul__

    def __imul__(self: Self, s: int | Self):
        if isinstance(s, int):
            self.x *= s
            self.y *= s
            return self
        if isinstance(s, Vector2):
            self.x *= s.x
            self.y *= s.y
            return self
        else:
            raise TypeError()

    __irmul__ = __imul__

    def __matmul__ (self: Self, s: Self) -> int:
        return self.x * s.x + self.y * s.y

    def __neg__(self: Self) -> Self:
        return self * -1

    def __repr__(self: Self) -> str:
        return f"V2({self.x}, {self.y})"

    def __iter__(self: Self):
        yield self.x
        yield self.y