"""Sweep line algorithm for finding the intersections of line segments."""

class Point():
    """A point in the plane."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        """Return True if the point is less than the other point."""
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        """Return True if the points are equal."""
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """Return a string representation of the point."""
        return f"({self.x}, {self.y})"


class Segment():
    """A line segment in the plane."""
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        # Assert that the segment is not vertical
        if self.start.x == self.end.x:
            raise ValueError("The start and end points of a segment cannot be the same.")
        self.slope = (end.y - start.y) / (end.x - start.x)

    def __repr__(self):
        """Return a string representation of the segment."""
        return f"({self.start}, {self.end})"

    def intersection(self, other: 'Segment') -> Point | bool:
        """
        Check if this segment intersects another segment.
        Use the determinant of the matrix formed by the start and end points of the segments.
        """
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        x3, y3 = other.start.x, other.start.y
        x4, y4 = other.end.x, other.end.y

        # Use the parametric form of the line to find the intersection point
        # t and u are the parameters for the two segments
        # x1 + t(x2 - x1) = x3 + u(x4 - x3)
        # y1 + t(y2 - y1) = y3 + u(y4 - y3)
        # Solve for t and u

        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / det
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / det

        # Check if the intersection point is within the segments
        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)

            return Point(intersection_x, intersection_y)



class Event():
    """An event in the sweep line algorithm."""
    def __init__(self, x: float, event_type: int, segment_id: int):
        self.x = x
        self.event_type = event_type
        self.segment_id = segment_id

    def __repr__(self):
        return f"(segment={self.segment_id}, type={self.event_type}, point.x {self.x})"

def solve(segments: list[Segment]) -> list[Point]:
    """Find the intersection points of a set of line segments."""
    events = []

    # Add all the start and end points of the segments to the events list
    for i, segment in enumerate(segments):
        if segment.start.x > segment.end.x: # swap if start is greater than end
            segment.start, segment.end = segment.end, segment.start
        events.append(Event(segment.start.x, 1, i)) # 1 for start
        events.append(Event(segment.end.x, -1, i)) # -1 for end

    # Sort the events by x-coordinate and event type
    events.sort(key=lambda x: (x.x, -x.event_type))
    print(events)

    status: list[Segment] = [] # list of segments that are currently intersecting the sweep line
    intersections: list[Point] = [] # list of intersection points

    # Process the events one by one from left to right
    for event in events:
        segment = segments[event.segment_id]
        if event.event_type == 1:
            status.append(segment) # add segment to status
            status.sort(key=lambda x: x.slope) # sort by slope

            if len(status) > 1:
                if status[-1].slope == status[-2].slope: # Compare slopes of the last two segments
                    if status[-1].start.x > status[-2].start.x:
                        status[-1], status[-2] = status[-2], status[-1]
                inter = status[-1].intersection(status[-2])
                if inter:
                    intersections.append(inter)

        else:
            status.remove(segment)
            if status:
                if status[-1].slope == segment.slope:
                    inter = status[-1].intersection(segment)
                    if inter:
                        intersections.append(inter)
    return intersections

# Example
segment1 = Segment(Point(1, 1), Point(4, 4))
segment2 = Segment(Point(1, 3), Point(3, 1))
segment3 = Segment(Point(3, 1), Point(5, 3))
segment4 = Segment(Point(3, 2), Point(5, 0))

segments = [segment3, segment4]
intersections = solve(segments)
for intersection in intersections:
    print(intersection)
# Output:
# (2.0, 2.0)
