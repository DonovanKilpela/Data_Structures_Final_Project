"""
These are the unit test for my project 
"""
import unittest
import tkinter as tk
from AmazonProjectKilpela import *


class TestTrailerMethods(unittest.TestCase):
    def setUp(self):
        self.trailer = Trailer("AMZN201", 2000, 1450, 25000)

    def test_get_packages_left(self):
        self.assertEqual(self.trailer.get_packages_left(), 550)

    def test_push_and_pop_packages_left(self):
        self.trailer.push_packages_left()
        self.assertEqual(self.trailer.pop_packages_left(), 550)

    def test_less_than_comparison(self):
        trailer1 = Trailer("AMZN201", 2000, 1450, 25000)
        trailer2 = Trailer("AMZN124", 5000, 4195, 30000)
        self.assertLess(trailer1, trailer2)

class TestTrailerGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.trailers = [
            Trailer("AMZN201",2000, 1450, 25000),
            Trailer("AMZN124",5000, 4195, 30000)
        ]
        self.gui = TrailerGUI(self.root, self.trailers)

    def test_create_gui(self):
        # Check if the GUI was created without errors
        self.assertTrue(self.gui.canvas.winfo_exists())

    # Remove the test_add_packages method

    def tearDown(self):
        self.root.destroy()

class TestTrailerSorting(unittest.TestCase):
    def setUp(self):
        self.trailers = [
            Trailer("AMZN201", 2000, 1450, 25000),
            Trailer("AMZN124", 5000, 4195, 30000),
            Trailer("AMZN412", 935, 100, 1654),
            Trailer("AMZN101", 2612, 2612, 28000),
            Trailer("AMZN314", 5123, 4312, 40012),
            Trailer("AMZN573", 5412, 1235, 6340), 
            Trailer("AMZN231", 6000, 4123, 12002),
            Trailer("AMZN512", 20123, 123, 600),
            Trailer("AMZN126", 6481, 3153, 30230),
            Trailer("AMZN812", 712, 521, 1400),
            Trailer("AMZN312", 1023, 745, 15000),
            Trailer("AMZN718", 3041, 2981, 12400)
        ]

    def test_sort_by_packages_loaded(self):
        sorted_trailers = sorted(self.trailers, key=lambda trailer: trailer.packages_loaded)
        self.assertEqual(sorted_trailers[0].packages_loaded, 100)

    def test_sort_by_packages_expected(self):
        sorted_trailers = sorted(self.trailers, key=lambda trailer: trailer.packages_expected)
        self.assertEqual(sorted_trailers[0].packages_expected, 712)

    def test_sort_by_packages_left(self):
        initial_packages_left = [550, 805, 835, 0, 811, 4177, 1877, 20000, 3328, 191, 278, 60]
        sorted_trailers = sorted(self.trailers, key=lambda trailer: trailer.get_packages_left())
        self.assertEqual(sorted_trailers[0].get_packages_left(), min(initial_packages_left))

class TestTrailerQueueOperations(unittest.TestCase):
    def setUp(self):
        self.trailers = [
            Trailer("AMZN201", 2000, 1450, 25000),
            Trailer("AMZN124", 5000, 4195, 30000),
            Trailer("AMZN412", 935, 100, 1654)
        ]
        self.trailer_gui = TrailerGUI(tk.Tk(), self.trailers)

    def test_add_trailer(self):
        new_trailer = Trailer("AMZN999", 1000, 500, 20000)
        self.trailer_gui.trailers.put(new_trailer)
        self.assertEqual(self.trailer_gui.trailers.qsize(), len(self.trailers) + 1)

    def test_remove_trailer(self):
        self.trailer_gui.trailers.get()  # Remove the first trailer
        self.assertEqual(self.trailer_gui.trailers.qsize(), len(self.trailers) - 1)

    def test_queue_empty(self):
        empty_queue = PriorityQueue()
        self.assertTrue(empty_queue.empty())

class TestTrailerStack(unittest.TestCase):
    def setUp(self):
        # Create a Trailer instance
        self.trailer = Trailer("AMZN201", 2000, 1450, 25000)

    def test_push_packages_left(self):
        # Push the number of packages left onto the stack
        self.trailer.push_packages_left()
        # Check if the stack is updated correctly
        self.assertEqual(self.trailer.packages_left_stack, [550])

    def test_pop_packages_left(self):
        # Push some values onto the stack
        self.trailer.packages_left_stack = [550, 700, 900]
        # Pop the top of the stack
        popped_value = self.trailer.pop_packages_left()
        # Check if the popped value is correct
        self.assertEqual(popped_value, 900)
        # Check if the stack is updated correctly
        self.assertEqual(self.trailer.packages_left_stack, [550, 700])

    def test_pop_empty_stack(self):
        # Try to pop from an empty stack
        popped_value = self.trailer.pop_packages_left()
        # Check if None is returned when popping from an empty stack
        self.assertIsNone(popped_value)
        # Check if the stack remains empty
        self.assertEqual(self.trailer.packages_left_stack, [])

if __name__ == '__main__':
    unittest.main()
