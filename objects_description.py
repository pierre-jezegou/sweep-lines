"""Generate TikZ code for objects description: present classes."""
from additional_algorithms.class_description import ObjectClassToTikz
from sweep_lines import Segment, Point, Event, solve, naive_solve, semi_naive_solve, segments

if __name__ == "__main__":
    # Example
    objects = [
        ObjectClassToTikz(Segment(Point(1, 1), Point(2, 2)), hidden_methods=True),
        ObjectClassToTikz(Point(1, 1), hidden_methods=True),
        ObjectClassToTikz(Event(Point(1, 1),
                            Segment(Point(2, 2),
                            Point(3, 3)),
                            "start"),
                          hidden_methods=True),
    ]
    for element in objects:
        element.save_drawing()
