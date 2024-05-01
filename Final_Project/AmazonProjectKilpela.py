"""
Name : AmazonProjectKilpela.py
Author: Donovan Kilpela
Created : 04/30/24
Course: CIS 152 - Data Structure
Version: 1.0
OS: Windows 11
IDE: VS Code 1.88
Copyright : This is my own original work
based on specifications issued by our instructor
Description : This project has two data structures and a sort method 
            The first data structure is a Priority Queue, the second 
            is a Stack that the number of packages goes into 
            The sort method is selection sort. 
            Input: N/a
            Output: GUI with trailer information and leaving times 
            BigO: N
Academic Honesty: I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified. I have not given other fellow student(s) access
to my program.
"""


import tkinter as tk
from queue import PriorityQueue
# import random

# Creates a truck class that has trailer id, expeceted packges and packages loaded
class Truck:
    def __init__(self, trailer_id, packages_expected, packages_loaded=0):
        self.trailer_id = trailer_id
        self.packages_expected = packages_expected
        self.packages_loaded = packages_loaded

# Creates a Packages that inherits from Truck but adds weight 
class Package(Truck):
    def __init__(self, trailer_id, packages_expected, packages_loaded, weight):
        super().__init__(trailer_id, packages_expected, packages_loaded)
        self.weight = weight  # in pounds

# Creates a Trailer class that inherits from Package and holds the stack 
class Trailer(Package):
    def __init__(self, trailer_id, packages_expected, packages_loaded, weight):
        super().__init__(trailer_id, packages_expected, packages_loaded, weight)
        self.packages_left_stack = []

    # This method will get the number of packges left in the trailer 
    def get_packages_left(self):
        return self.packages_expected - self.packages_loaded

    # This method will get the number of packages left on the stack 
    def push_packages_left(self):
        self.packages_left_stack.append(self.get_packages_left())

    # This method will remove the top element in the stack 
    def pop_packages_left(self):
        if self.packages_left_stack:
            return self.packages_left_stack.pop()
        else:
            return None

    # This method define less than comparison based on packages left 
    def __lt__(self, other):
        return self.get_packages_left() < other.get_packages_left()


# Creates the Trailer Gui Class that will hold all of the GUI elements 
class TrailerGUI:
    def __init__(self, root, trailers):
        self.root = root
        self.trailers = PriorityQueue()
        self.packages_left_stack = []
        self.canvas = tk.Canvas(self.root, bg="#908A89", width=1000, height=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.truck_boxes = []  # Store truck box IDs for updating colors
        self.trailer_texts = []  # Store trailer text IDs for updating packages info
        self.create_gui(trailers)

    # This method will create the GUI and give the groups labels to make the GUI more organized 
    def create_gui(self, trailers):
        x_spacing = 200
        y_spacing = 150
        group_labels = {
            (0, 1, 2, 3): "Trailers Leaving at 6pm",
            (4, 5, 6, 7): "Trailers leaving at 2pm",
            (8, 9, 10, 11): "Trailers leaving at 10am"
        }

        try:
            # This sorts trailers based on their percentages full
            sorted_trailers = self.selection_sort(trailers)

            # This iterates over the sorted trailers to create the GUI elements 
            for i, trailer in enumerate(sorted_trailers):
                self.trailers.put(trailer)
                self.packages_left_stack.append(trailer.get_packages_left())

                # This calculates positions for the trailer display 
                x = (i % 4) * x_spacing + 100
                y = (i // 4) * y_spacing + 100

                # This determines group membership
                for group, label in group_labels.items():
                    if i in group:
                        is_group1 = group == (0, 1, 2, 3)
                        break

                # This will draw labeled boxes around specific groups of trailers
                for group, label in group_labels.items():
                    if i in group:
                        group_x = min(x for x, _ in [((x % 4) * x_spacing + 100, (x // 4) * y_spacing + 100) for x in group])
                        group_y = min(y for _, y in [((x % 4) * x_spacing + 100, (x // 4) * y_spacing + 100) for x in group])
                        group_width = max(x for x, _ in [((x % 4) * x_spacing + 100, (x // 4) * y_spacing + 100) for x in group]) - group_x + 150
                        group_height = max(y for _, y in [((x % 4) * x_spacing + 100, (x // 4) * y_spacing + 100) for x in group]) - group_y + 100
                        self.canvas.create_rectangle(group_x - 10, group_y - 10, group_x + group_width + 10, group_y + group_height + 10, outline="#333333", width=2)
                        self.canvas.create_text(group_x + group_width / 2, group_y - 20, text=label, font=("Arial", 12), fill="#333333")

                # This draws truck body with gradient fill and labels
                percentage_loaded = trailer.packages_loaded / trailer.packages_expected
                if is_group1:
                    # Green gradient for group 1
                    fill_color = "#6cb74a" if percentage_loaded == 1.0 else "#f6d34a" if percentage_loaded >= 0.75 else "#f6894a" if percentage_loaded >= 0.5 else "#f63a3a"
                else:
                    # Other groups use solid colors
                    if percentage_loaded == 1.0:
                        fill_color = "#6cb74a"  # 100% full
                    elif percentage_loaded >= 0.75:
                        fill_color = "#f6d34a"  # 75%-100% full
                    elif percentage_loaded >= 0.5:
                        fill_color = "#f6894a"  # 50%-75% full
                    else:
                        fill_color = "#f63a3a"  # 0%-50% full

                truck_id = self.canvas.create_rectangle(x, y, x + 120, y + 80, outline="#333333", fill=fill_color)
                self.canvas.create_text(x + 60, y + 40, text=f"Truck {i+1}", font=("Arial", 10), fill="#333333")

                # Draw wheels
                wheel_positions = [(x + 20, y + 85), (x + 100, y + 85)]
                for wheel_x, wheel_y in wheel_positions:
                    self.canvas.create_oval(wheel_x - 10, wheel_y - 10, wheel_x + 10, wheel_y + 10, fill="#333333")

                # Display trailer ID and packages info
                self.canvas.create_text(x + 60, y + 20, text=f"{trailer.trailer_id}", font=("Arial", 10), fill="#333333")
                self.canvas.create_text(x + 60, y + 60, text=f"Loaded: {trailer.packages_loaded}/{trailer.packages_expected}\nPackages left: {trailer.packages_expected - trailer.packages_loaded}", font=("Arial", 8), fill="#333333")

            # This was supposed to make it so we can add packages to the GUI but I couldn't figure it out 
            # Add form to add packages
            # self.trailer_id_entry = tk.Entry(self.root, width=20)
            # self.trailer_id_entry.pack()

            # self.packages_entry = tk.Entry(self.root, width=20)
            # self.packages_entry.pack()

            # add_button = tk.Button(self.root, text="Add Packages", command=self.add_packages)
            # add_button.pack()

        except Exception as e:
            # Handle any unexpected errors
            print(f"Error: {e}")

    # This is the sort for the program 
    def selection_sort(self, trailers):
        trailers_list = list(trailers)
        n = len(trailers_list)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                percentage_i = trailers_list[i].packages_loaded / trailers_list[i].packages_expected
                percentage_j = trailers_list[j].packages_loaded / trailers_list[j].packages_expected
                if percentage_j < percentage_i:
                    min_idx = j
            trailers_list[i], trailers_list[min_idx] = trailers_list[min_idx], trailers_list[i]
        return trailers_list


# Defines the trailers
trailers = [
    Trailer("AMZN201",2000, 1450, 25000),
    Trailer("AMZN124",5000, 4195, 30000),
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

# Create the GUI
root = tk.Tk()
root.title("Trailer IDs")
root.geometry("1000x800")
gui = TrailerGUI(root, trailers)
root.mainloop()

