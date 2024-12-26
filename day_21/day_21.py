import re
from math import inf
from enum import Enum

from typing import Self
from collections import defaultdict
from vector2 import Vector2

class DirectionButton(Enum):
    Up    = '^'
    Right = '>'
    Down  = 'v'
    Left  = '<'
    A     = 'A'

class NumericButton(Enum):
    Zero  = '0'
    One   = '1'
    Two   = '2'
    Three = '3'
    Four  = '4'
    Five  = '5'
    Six   = '6'
    Seven = '7'
    Eight = '8'
    Nine  = '9'
    A     = 'A'

with open('input') as input:
    codes: list[str] = input.read().splitlines()
    codes: list[tuple[list[NumericButton], int]] = [([*map(NumericButton, code)], int(re.search(r'\d+', code).group())) for code in codes]

class Keypad:
    pad            : tuple[tuple[None | DirectionButton | NumericButton], ...]
    button_location: dict[DirectionButton | NumericButton, Vector2]

    @classmethod
    def get_button_location(self, button: DirectionButton | NumericButton) -> Vector2:
        if button not in self.button_location:
            self.button_location[button] = next(Vector2(i, line.index(button)) for i, line in enumerate(self.pad) if button in line)
        return self.button_location[button]
    
    def __init__(self, parent: Self):
        self.parent: Self = parent
        self.M: dict[tuple[NumericButton | DirectionButton, ...], int] = defaultdict(lambda: 0)
    
    @classmethod
    def A_button(self) -> NumericButton | DirectionButton:
        pass

    @classmethod
    def forbidden(self) -> Vector2:
        pass

    def get_cost(self, button_sequences: list[list[NumericButton | DirectionButton]]) -> int:

        for buttons_sequence in button_sequences:
            if tuple(buttons_sequence) not in self.M:
                if self.parent:
                    self.calculate_cost(buttons_sequence)
                else:
                    self.M[tuple(buttons_sequence)] = len(buttons_sequence)
        return sum(self.M[tuple(buttons)] for buttons in button_sequences)

    def calculate_cost(self, button_sequence: list[NumericButton | DirectionButton]) -> int:

        cursor: Vector2 = self.get_button_location(self.A_button())
        
        for button in button_sequence:
            button_location: Vector2 = self.get_button_location(button)
            delta: Vector2 = button_location - cursor

            v: list[DirectionButton] = [DirectionButton.Up   if delta.x < 0 else DirectionButton.Down ] * abs(delta.x)
            h: list[DirectionButton] = [DirectionButton.Left if delta.y < 0 else DirectionButton.Right] * abs(delta.y)

            self.M[tuple(button_sequence)] += min(
                self.parent.get_cost([h + v + [DirectionButton.A]]) if cursor + delta.y_project() != self.forbidden() else inf,
                self.parent.get_cost([v + h + [DirectionButton.A]]) if cursor + delta.x_project() != self.forbidden() else inf
            )

            cursor = button_location

class NumericKeypad(Keypad):

    pad: tuple[tuple[None | DirectionButton | NumericButton], ...] = (
        (NumericButton.Seven, NumericButton.Eight, NumericButton.Nine ),
        (NumericButton.Four , NumericButton.Five , NumericButton.Six  ),
        (NumericButton.One  , NumericButton.Two  , NumericButton.Three),
        (None               , NumericButton.Zero , NumericButton.A    )
    )
    button_location: dict[NumericButton, Vector2] = dict()
    
    @classmethod
    def A_button(self) -> NumericButton:
        return NumericButton.A
    
    @classmethod
    def forbidden(self) -> Vector2:
        return Vector2(3, 0)

class DirectionalKeypad(Keypad):

    pad: tuple[tuple[None | DirectionButton | NumericButton], ...] = (
        (None                , DirectionButton.Up  , DirectionButton.A    ),
        (DirectionButton.Left, DirectionButton.Down, DirectionButton.Right)
    )
    button_location: dict[DirectionButton, Vector2] = dict()

    @classmethod
    def A_button(self) -> DirectionButton:
        return DirectionButton.A
    
    @classmethod
    def forbidden(self) -> Vector2:
        return Vector2(0, 0)

def solve_with_k_robots(codes: list[tuple[list[NumericButton], int]], k: int) -> int:

    human: DirectionalKeypad  = DirectionalKeypad(None      )
    parent: DirectionalKeypad = human
    for _ in range(k):
        new_robot: DirectionalKeypad = DirectionalKeypad(parent)
        parent = new_robot
    robot_NK: NumericKeypad = NumericKeypad(parent)

    return sum(
        robot_NK.get_cost([buttons]) * number
        for buttons, number in codes
    )

with open('output', 'w') as output:
    output.write( str(solve_with_k_robots(codes,  2)) + '\n')
    output.write( str(solve_with_k_robots(codes, 25)) + '\n')