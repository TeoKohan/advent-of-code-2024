import re
import numpy as np

from vector2 import Vector2
from itertools import count
from copy import deepcopy
from PIL import Image

class Robot():
    def __init__(self, position_x: int, position_y: int, velocity_x: int, velocity_y: int):
        self.position: Vector2 = Vector2(position_x, position_y)
        self.velocity: Vector2 = Vector2(velocity_x, velocity_y)
    
    def move(self, steps: int):
        self.position += self.velocity * steps

    def fit_into(self, space: Vector2):
        self.position.x %= space.x
        self.position.y %= space.y

width, height = 101, 103
with open('input') as input:
    robots: list[str] = input.read().splitlines()
    robots: list[list[str]] = [[*map(int, re.findall(r'-?\d+', robot))] for robot in robots]
    robots: list[Robot] = [Robot(*robot) for robot in robots]
    
def robots_print(robots) -> str:
    display = [[0] * width for _ in range(height)]

    for x, y in robots:
        display[y][x] = min(display[y][x] + 64, 255)

    A = np.array(display, dtype=np.uint8)
    img = Image.fromarray(A)
    img.save('output.png')

def quartiles(robots: list[Robot]) -> int:
    Q1, Q2, Q3, Q4 = 0, 0, 0, 0
    for robot in robots:
        robot.move(100)
        robot.fit_into(Vector2(width, height))
        if robot.position.x > width // 2 and robot.position.y > height // 2:
            Q1 += 1
        elif robot.position.x < width // 2 and robot.position.y > height // 2:
            Q2 += 1
        elif robot.position.x < width // 2 and robot.position.y < height // 2:
            Q3 += 1
        elif robot.position.x > width // 2 and robot.position.y < height // 2:
            Q4 += 1
    return Q1 * Q2 * Q3 * Q4


def search_tree(robots: list[Robot]) -> int:
    for i in count(1):
        for robot in robots:
            robot.move(1)
            robot.fit_into(Vector2(width, height))
        
        A = np.array([list(robot.position) for robot in robots], dtype=np.uint16)
        if np.var(A) < 400:
            robots_print(A)
            return i
        
with open('output', 'w') as output:
    output.write( str(quartiles(deepcopy(robots))) + '\n')
    output.write( str(search_tree(deepcopy(robots))) + '\n')