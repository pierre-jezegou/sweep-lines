import random
import time
from jinja2 import Template
from sweep_lines import Segment, Point, solve, naive_solve, semi_naive_solve

sizes = [i for i in range(1, 500, 5)]
NUMBER_OF_TESTS = 20

BOUNDARY = 10000

TEMPLATE_NAME: str = 'additional_algorithms/template_performances.tex.jinja'

class Test():
    """Class to store the results of a test."""
    def __init__(self, 
                 size: int,
                 sweep_time: float,
                 naive_time: float,
                 semi_naive_time: float,
                 sweep_intersections: int,
                 naive_intersections: int,
                 semi_naive_intersections: int):
        self.size = size
        self.sweep_time = sweep_time
        self.naive_time = naive_time
        self.semi_naive_time = semi_naive_time
        self.sweep_intersections = sweep_intersections
        self.naive_intersections = naive_intersections
        self.semi_naive_intersections = semi_naive_intersections
        self.percentage_swl_detected_intersections = sweep_intersections / naive_intersections if naive_intersections > 0 else 0
        self.percentage_sn_detected_intersections = semi_naive_intersections / naive_intersections if naive_intersections > 0 else 0


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
    print("Starting retrieval of performances")
    for size in sizes:
        print(f"\tSize: {size}")
        for _ in range(NUMBER_OF_TESTS):
            segments = generate_random_segments(size)
            start_time = time.process_time()
            result = solve(segments)
            end_time = time.process_time()
            sweep_intersections = len(result)
            sweep_time = end_time - start_time

            start_time = time.process_time()
            result_naive = naive_solve(segments)
            end_time = time.process_time()
            naive_intersections = len(result_naive)
            naive_time = end_time - start_time

            start_time = time.process_time()
            result_semi_naive = semi_naive_solve(segments)
            end_time = time.process_time()
            semi_naive_intersections = len(result_semi_naive)
            semi_naive_time = end_time - start_time

            performances.append(Test(size=size,
                                     sweep_time=sweep_time,
                                     naive_time=naive_time,
                                     sweep_intersections=sweep_intersections,
                                     naive_intersections=naive_intersections,
                                     semi_naive_intersections=semi_naive_intersections,
                                     semi_naive_time=semi_naive_time))

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


def plot_pgf(series: list[TestSerie],
             title: str = "",
             xlabel: str = "Number of segments",
             ylabel: str = "Performance ?"
             ) -> str:
    """Plot the performances in a PGFPlots plot."""
    with open(TEMPLATE_NAME, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_template = template.render(metrics=[serie.plot_pgf() for serie in series],
                                        title=title,
                                        xlabel=xlabel,
                                        ylabel=ylabel)
    return rendered_template

# series = [
#         TestSerie("Naive CPU Time", "naive_time", performances, "red"),
#         TestSerie("Sweep CPU Time", "sweep_time", performances, "blue"),
#         TestSerie("Semi-naive CPU Time", "semi_naive_time", performances, "orange"),
#         # TestSerie("Naive intersections", "naive_intersections", performances, "red"),
#         # TestSerie("Sweep intersections", "sweep_intersections", performances, "blue"),
#         # TestSerie("Percentage of correct intersections", "percentage_detected_intersections", performances, "blue"),
#     ]

def generate(data: dict):
    print(f"Generating {data['filename']}...")
    rendered_template = plot_pgf(data["series"], data["title"], data["xlabel"], data["ylabel"])
    with open(data["filename"], 'w') as file:
        file.write(rendered_template)

ROOT_PLOTS = 'documentation/images/plots'
if __name__ == "__main__":
    data = get_performances()
    plots_to_save = [
        {
            'filename': 'performances.tex',
            'title': 'CPU Time for different algorithms',
            'xlabel': 'Number of segments',
            'ylabel': 'Time (s)',
            'series': [
                TestSerie("Naive CPU Time", "naive_time", data, "red"),
                TestSerie("Sweep CPU Time", "sweep_time", data, "blue"),
                TestSerie("Semi-naive CPU Time", "semi_naive_time", data, "orange"),
            ]
        },
        {
            'filename': 'percentage_of_detection.tex',
            'title': 'Percentage of detected intersections compared to the naive algorithm',
            'xlabel': 'Number of segments',
            'ylabel': '% of detected intersections',
            'series': [
                TestSerie("Sweep lines", "percentage_swl_detected_intersections", data, "blue"),
                TestSerie("Semi-naive algorithm", "percentage_sn_detected_intersections", data, "orange"),
            ]
        }
    ]
    for plot in plots_to_save:
        plot['filename'] = f"{ROOT_PLOTS}/{plot['filename']}"
        generate(plot)
