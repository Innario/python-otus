from .figure import Figure


class Rectangle(Figure):

    def __init__(self, side1, side2):
        super().__init__(side1, side2)
        self.side1 = side1
        self.side2 = side2
        self.name = "Rectangle"

    @property
    def area(self):
        return self.side1 * self.side2

    @property
    def perimeter(self):
        return 2 * self.side1 + 2 * self.side2
