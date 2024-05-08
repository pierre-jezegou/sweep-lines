from jinja2 import Template
import random

TEMPLATE_NAME = 'additional_algorithms/template_2D_intersections.tex.jinja'
NUMBER_OF_SEGMENTS = 10

LOWER_BOUND = 0
UPPERBOUND = 10


def generate_random_value(lower_bound: float, upper_bound: float) -> float:
    """
    Generate a random float value within the specified range.

    Args:
        lower_bound (float): The lower bound of the range.
        upper_bound (float): The upper bound of the range.

    Returns:
        float: A random float value within the specified range.
    """
    return random.uniform(lower_bound, upper_bound)


def format_point(point: tuple[float, float]) -> str:
    """
    Formats a point as a string in the format "(axis cs:x, y)".
    """
    return f"(axis cs:{point[0]}, {point[1]})"


def plot_segments(segments: list, intersections: list[tuple[float, float]] | None) -> None:
    """
    Plot the given segments and intersections using a Jinja template.

    Args:
        segments (list): A list of segments to be plotted.
        intersections (list[tuple[float, float]] | None):
            A list of intersections to be plotted, or None if there are no intersections.

    Returns:
        None
    """

    # Load the Jinja template from a file
    with open(TEMPLATE_NAME, 'r') as file:
        template_content = file.read()

    template = Template(template_content)

    segments_str = [' '.join(map(str, segment)) for segment in segments]

    if intersections is not None:
        intersections_str = [format_point(intersection) for intersection in intersections]
    else:
        intersections_str = ''

    rendered_template = template.render(segments=segments_str, intersections=intersections_str)

    return rendered_template



if __name__ == '__main__':
    # Define the points to be added to the template
    segments = [[(generate_random_value(LOWER_BOUND, UPPERBOUND),
                generate_random_value(LOWER_BOUND, UPPERBOUND)),
                (generate_random_value(LOWER_BOUND, UPPERBOUND),
                generate_random_value(LOWER_BOUND, UPPERBOUND))
                ] for _ in range(NUMBER_OF_SEGMENTS)]

    # intersections = [(10, 10), (20, 20), (80, 80)]
    intersections = None

    print(plot_segments(segments, intersections))
