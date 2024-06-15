import random
import time
from jinja2 import Template
from sweep_lines import Segment, Point, solve, naive_solve

# sizes = [10, 20, 30 , 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
sizes = [i for i in range(10, 501, 10)]
NUMBER_OF_TESTS = 20

BOUNDARY = 100

TEMPLATE_NAME: str = 'additional_algorithms/template_performances.tex.jinja'

class Test():
    """Class to store the results of a test."""
    def __init__(self, 
                 size: int,
                 sweep_time: float,
                 naive_time: float,
                 sweep_intersections: int,
                 naive_intersections: int):
        self.size = size
        self.sweep_time = sweep_time
        self.naive_time = naive_time
        self.sweep_intersections = sweep_intersections
        self.naive_intersections = naive_intersections
        self.percentage_detected_intersections = sweep_intersections / naive_intersections


def generate_random_segments(size) -> list[Segment]:
    """Generate a list of random segments."""
    segments = []
    for _ in range(size):
        x1, x2 = None, None
        while x1 == x2:
            x1, y1 = random.uniform(0, BOUNDARY), random.uniform(0, BOUNDARY)
            x2, y2 = random.uniform(0, BOUNDARY), random.uniform(0, BOUNDARY)
        segment = Segment(Point(x1, y1), Point(x2, y2))
        segments.append(segment)
    return segments

def get_performances() -> list[dict]:
    """Mesearure the performance of the sweep line algorithm."""
    performances = []

    for size in sizes:
        for _ in range(NUMBER_OF_TESTS):
            segments = generate_random_segments(size)
            start_time = time.time()
            result = solve(segments)
            end_time = time.time()
            sweep_intersections = len(result)
            sweep_time = end_time - start_time

            start_time = time.time()
            result_naive = naive_solve(segments)
            end_time = time.time()
            naive_intersections = len(result_naive)
            naive_time = end_time - start_time

            performances.append(Test(size=size,
                                     sweep_time=sweep_time,
                                     naive_time=naive_time,
                                     sweep_intersections=sweep_intersections,
                                     naive_intersections=naive_intersections))

    return performances

class TestSerie:
    def __init__(self, title: str, metric: str, raw_data: list[Test], color: str):
        self.title = title
        self.metric = metric
        self.color = color
        self.data = [(test.size, getattr(test, metric)) for test in raw_data]

    def data_to_str(self):
        return "".join([f"({size}, {time})\n" for size, time in self.data])

    def plot_pgf(self):
        return f"""\\addplot[only marks, mark=x, color={self.color}] coordinates {{
            {self.data_to_str()}
            }};
            \\addlegendentry{{{self.title}}};"""


def plot_pgf(performances: list[Test]) -> str:
    """Plot the performances in a PGFPlots plot."""
    series = [
        # TestSerie("Naive CPU Time", "naive_time", performances, "red"),
        # TestSerie("Sweep CPU Time", "sweep_time", performances, "blue"),
        # TestSerie("Naive intersections", "naive_intersections", performances, "red"),
        # TestSerie("Sweep intersections", "sweep_intersections", performances, "blue"),
        TestSerie("Percentage of correct intersections", "percentage_detected_intersections", performances, "blue"),
    ]

    with open(TEMPLATE_NAME, 'r') as file:
        template_content = file.read()

    template = Template(template_content)

    rendered_template = template.render(metrics=[serie.plot_pgf() for serie in series])

    return rendered_template



if __name__ == "__main__":
    result = get_performances()
    print(plot_pgf(result))
