import random

class Pi:
    def __init__(self, radius=1, precision=2):
        self.radius = radius
        self.precision = precision
        self.lower = -radius
        self.upper = radius

    # Generates a random point
    def generatePoint(self):
        x_coordinate = round(
            random.uniform(self.lower, self.upper),
            self.precision
        )
        y_coordinate = round(
            random.uniform(self.lower, self.upper),
            self.precision
        )
        return [x_coordinate, y_coordinate]

    # Returns True is point lies inside the circle
    def isInsideCircle(self, coordinates):
        [x,y] = coordinates
        if x**2 + y**2 <= self.radius**2:
            return True
        return False

    def calculatePi(self, circle_hits, total):
        return (4*circle_hits)/total

def run(iterations):
    pi = Pi(precision=4)
    circle_hits = 0
    for i in range(iterations):
        point = pi.generatePoint()
        if pi.isInsideCircle(point):
            circle_hits += 1

    print('Estimated Pi: ', pi.calculatePi(circle_hits, iterations))


