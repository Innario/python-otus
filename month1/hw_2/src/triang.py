import math

from .figure import Figure


class Triangle(Figure):

    def __init__(self, side1, side2, side3):
        super().__init__(side1, side2, side3)
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        if side1 + side2 <= side3 or side1 + side3 <= side2 or side2 + side3 <= side1:
            raise ValueError("The triangle inequality is not satisfied")
        self.name = "Triangle"

    @property
    def area(self):
        s = (self.side1 + self.side2 + self.side3) / 2.0
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))

    @property
    def perimeter(self):
        return self.side1 + self.side2 + self.side3
