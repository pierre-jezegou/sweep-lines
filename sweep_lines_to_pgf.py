from jinja2 import Template
from sweep_lines import Segment, Point, solve

TEMPLATE_NAME: str = 'additional_algorithms/template_2D_intersections.tex.jinja'

def segments_to_pgf(segments: list[Segment], display_intersections: bool = True) -> None:
    """Convert a list of segments to a PGFPlots plot."""
    intersections = solve(segments) if display_intersections else []

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
    # segment1 = Segment(Point(1, 1), Point(4, 4))
    # segment2 = Segment(Point(1, 3), Point(3, 1))
    # segment3 = Segment(Point(3, 1), Point(5, 3))
    # segment4 = Segment(Point(3, 2), Point(5, 0))

    # segments = [segment1, segment2, segment3, segment4]

    # Genetate 100 random segments
    import random
    segments = []
    for _ in range(10):
        x1, x2 = None, None
        while x1 == x2:
            x1, y1 = random.randint(0, 10), random.randint(0, 10)
            x2, y2 = random.randint(0, 10), random.randint(0, 10)
        segment = Segment(Point(x1, y1), Point(x2, y2))
        segments.append(segment)

    pgf = segments_to_pgf(segments)

    print(pgf)
