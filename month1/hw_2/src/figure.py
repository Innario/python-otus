class Figure:

    def __init__(self, *args):
        if any(x <= 0 for x in args):
            raise ValueError("All values should be > 0")

    @property
    def area(self):
        raise NotImplementedError("Area can't be calculated in base object")

    @property
    def perimeter(self):
        raise NotImplementedError("Perimeter can't be calculated in base object")

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise ValueError("Value isn't instance of class Figure")
        return self.area + figure.area

