from jinja2 import Template
from sweep_lines import Segment, Point, solve, naive_solve

TEMPLATE_NAME: str = 'additional_algorithms/template_2D_intersections.tex.jinja'

def segments_to_pgf(segments: list[Segment], display_intersections: bool = True) -> None:
    """Convert a list of segments to a PGFPlots plot."""
    intersections = solve(segments) if display_intersections else []
    
    intersections_naive = naive_solve(segments) if display_intersections else []
    
    if intersections != intersections_naive:
        print("The naive and sweep line algorithms do not return the same results.")
        print("Percetage of correct intersections: ", len(intersections) / len(intersections_naive))

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
    segments = [
        Segment(Point(1, 1), Point(4, 4)),
        Segment(Point(1, 3), Point(3, 1)),
        Segment(Point(3, 1), Point(5, 3)),
        Segment(Point(3, 2), Point(5, 0)),
        Segment(Point(2, 1), Point(2.6, 1.5)),
        Segment(Point(3, 4), Point(5, 2)),
        Segment(Point(3, 3.5), Point(4.5, 1.5)),
        Segment(Point(3.5, 2), Point(4.5, 3.5)),
        Segment(Point(2.5, 3), Point(3.5, 2.5)),
        Segment(Point(3, 2.5), Point(4, 3.5)),
        Segment(Point(1.5, 4), Point(1.75, 0))
    ]

    # Genetate 100 random segments
    # import random
    # segments = []
    # for _ in range(10):
    #     x1, x2 = None, None
    #     while x1 == x2:
    #         x1, y1 = random.randint(0, 10), random.randint(0, 10)
    #         x2, y2 = random.randint(0, 10), random.randint(0, 10)
    #     segment = Segment(Point(x1, y1), Point(x2, y2))
    #     segments.append(segment)

    pgf = segments_to_pgf(segments)

    print(pgf)
