import itertools
import math
import pytest

from ..src.circle import Circle
from ..src.triang import Triangle
from ..src.rectangle import Rectangle
from ..src.square import Square


@pytest.mark.parametrize("side1, side2, side3", [(12, 13, 14), (5, 6, 7)])
def test_triangle(side1, side2, side3):
    """
    * создание обьекта
    * корректность поля name
    * корректность поля area
    * корректность поля perimeter
    * корректность метода add_area
    """
    with pytest.raises(ValueError, match="All values should be > 0"):
        Triangle(-1, 2, 4)

    with pytest.raises(ValueError, match="The triangle inequality is not satisfied"):
        Triangle(1, 2, 4)

    triangle1 = Triangle(3, 4, 5)
    assert triangle1.name == "Triangle"
    assert triangle1.area == 6
    assert triangle1.perimeter == 12

    triangle2 = Triangle(side1, side2, side3)
    assert triangle2.name == "Triangle"
    assert triangle2.perimeter == side1 + side2 + side3
    s = triangle2.perimeter / 2.0
    assert triangle2.area == math.sqrt(s * (s - side1) * (s - side2) * (s - side3))

    assert triangle1.add_area(triangle2) == (triangle1.area + triangle2.area)
    assert triangle2.add_area(triangle1) == (triangle1.area + triangle2.area)


def test_circle():
    with pytest.raises(ValueError, match="All values should be > 0"):
        Circle(-5)

    circle1 = Circle(3)
    assert circle1.name == "Circle"
    assert circle1.area == math.pi * 3 ** 2
    assert circle1.perimeter == 2 * math.pi * 3

    circle2 = Circle(4)
    assert circle2.name == "Circle"
    assert circle2.area == math.pi * 4 ** 2
    assert circle2.perimeter == 2 * math.pi * 4

    assert circle1.add_area(circle2) == (circle1.area + circle2.area)
    assert circle2.add_area(circle1) == (circle1.area + circle2.area)


def test_rectangle():
    with pytest.raises(ValueError, match="All values should be > 0"):
        Rectangle(5, -4)

    rectangle1 = Rectangle(5, 8)
    assert rectangle1.area == 5 * 8
    assert rectangle1.perimeter == (2 * 5) + (2 * 8)

    rectangle2 = Rectangle(10, 5)
    assert rectangle2.name == "Rectangle"
    assert rectangle2.area == 10 * 5

    assert rectangle1.add_area(rectangle2) == (rectangle1.area + rectangle2.area)
    assert rectangle2.add_area(rectangle1) == (rectangle1.area + rectangle2.area)


def test_square():
    with pytest.raises(ValueError, match="All values should be > 0"):
        Square(-8)

    square1 = Square(8)
    assert square1.name == "Square"
    assert square1.area == 8 ** 2
    assert square1.perimeter == 8 * 4

    square2 = Square(5)
    assert square2.name == "Square"
    assert square2.area == 5 ** 2
    assert square2.perimeter == 5 * 4

    assert square1.add_area(square2) == (square1.area + square2.area)
    assert square2.add_area(square1) == (square1.area + square2.area)


def test_calc_area():
    figures = [Square(5), Rectangle(8, 4), Circle(6), Triangle(13, 84, 85)]
    for fig1, fig2 in itertools.permutations(figures, 2):
        assert fig1.add_area(fig2) == (fig1.area + fig2.area)
