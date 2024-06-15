import random
from jinja2 import Template
from sweep_lines import Segment, Point, solve, naive_solve, segments

TEMPLATE_NAME: str = 'additional_algorithms/template_2D_intersections.tex.jinja'

def segments_to_pgf(segments: list[Segment], display_intersections: bool = True) -> None:
    """Convert a list of segments to a PGFPlots plot."""
    intersections = solve(segments) if display_intersections else []

    intersections_naive = naive_solve(segments) if display_intersections else []
    # if intersections != intersections_naive:
    #     print("The naive and sweep line algorithms do not return the same results.")
    #     print("Percetage of correct intersections: ", (len(intersections) / len(intersections_naive)) if len(intersections_naive) > 0 else 0)
    # print("\\\\Number of intersections: ", len(intersections))
    # print("Number of intersections (naive): ", len(intersections_naive))
    # Load the Jinja template from a file
    with open(TEMPLATE_NAME, 'r') as file:
        template_content = file.read()

    template = Template(template_content)

    segments_str = [segment.segment_to_pgf() for segment in segments]

    if intersections is not None:
        intersections_str = [intersection.format_point() for intersection in intersections]
    else:
        intersections_str = ''

    rendered_template = template.render(segments=segments_str, intersections=intersections_str)

    return rendered_template


if __name__ == "__main__":
    # Example

    # Genetate 100 random segments

    # segments = []
    # for _ in range(20):
    #     x1, x2 = None, None
    #     while x1 == x2:
    #         x1, y1 = random.randint(0, 1000), random.randint(0, 1000)
    #         x2, y2 = random.randint(0, 1000), random.randint(0, 1000)
    #     segment = Segment(Point(x1, y1), Point(x2, y2))
    #     segments.append(segment)

    pgf = segments_to_pgf(segments)

    print(pgf)
