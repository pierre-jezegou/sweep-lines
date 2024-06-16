import random
from jinja2 import Template
from sweep_lines import Segment, Point, solve, naive_solve, semi_naive_solve

TEMPLATE_NAME: str = 'additional_algorithms/template_2D_intersections.tex.jinja'
ROOT_PLOT: str = 'documentation/images/plots'

def segments_to_pgf(segments: list[Segment],
                    title: str,
                    display_intersections: bool = True
                    ) -> None:
    """Convert a list of segments to a PGFPlots plot."""
    intersections = semi_naive_solve(segments) if display_intersections else []

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

    rendered_template = template.render(segments=segments_str,
                                        title=title,
                                        intersections=intersections_str)

    return rendered_template


def save_pgf(pgf: str, filename: str) -> None:
    """Save a PGFPlots plot to a file."""
    with open(filename, 'w') as file:
        file.write(pgf)

if __name__ == "__main__":
    # Complete example
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
        Segment(Point(1.5, 4), Point(1.75, 0)),
        Segment(Point(1, 2), Point(5, 3.35)),
    ]

    save_pgf(segments_to_pgf(segments, "Complete example"), f"{ROOT_PLOT}/complete_example.tex")

    # Colilnear intersecting segments
    segments = [
        Segment(Point(1, 1), Point(3, 3)),
        Segment(Point(2, 2), Point(5, 5))
        ]
    save_pgf(segments_to_pgf(segments, "Colinear intersecting segments"), f"{ROOT_PLOT}/colinear_segments.tex")

    # Point on segment
    segments = [
        Segment(Point(1, 3), Point(3, 1)),
        Segment(Point(2, 2), Point(5, 3))
        ]
    save_pgf(segments_to_pgf(segments, "Point on segment"), f"{ROOT_PLOT}/point_on_segment.tex")

    # Start segment = end other segment
    segments = [
        Segment(Point(1, 3), Point(3, 1)),
        Segment(Point(3, 1), Point(5, 3))
        ]
    save_pgf(segments_to_pgf(segments, "Start segment = end other segment"), f"{ROOT_PLOT}/start_segment_end_other.tex")

    # Genetate 100 random segments

    # segments = []
    # for _ in range(20):
    #     x1, x2 = None, None
    #     while x1 == x2:
    #         x1, y1 = random.randint(0, 1000), random.randint(0, 1000)
    #         x2, y2 = random.randint(0, 1000), random.randint(0, 1000)
    #     segment = Segment(Point(x1, y1), Point(x2, y2))
    #     segments.append(segment)
