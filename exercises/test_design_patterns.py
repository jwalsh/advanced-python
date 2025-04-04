import unittest

from design_patterns import ShapeFactory, Singleton


class TestDesignPatterns(unittest.TestCase):
    def test_singleton(self):
        s1 = Singleton()
        s2 = Singleton()
        self.assertEqual(s1, s2)

    def test_factory(self):
        factory = ShapeFactory()
        circle = factory.create_shape("circle")
        square = factory.create_shape("square")
        self.assertEqual(circle.draw(), "Drawing a circle")
        self.assertEqual(square.draw(), "Drawing a square")


if __name__ == "__main__":
    unittest.main()
