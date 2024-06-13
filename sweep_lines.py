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

    def __hash__(self) -> int:
        """Return the hash value of the point."""
        return hash((self.x, self.y))

    def format_point(self) -> str:
        """Return the point in the format (x, y)."""
        return f"(axis cs:{self.x}, {self.y})"


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

    def current_y(self, x: float) -> float:
        """Return the y-coordinate of the segment at the given x-coordinate."""
        return self.start.y + self.slope * (x - self.start.x)

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

    def segment_to_pgf(self) -> str:
        """Return the segment in the PGFPlots format."""
        return f"\\addplot[red, mark=*] coordinates {{{self.start} {self.end}}};"


class Event():
    """An event in the sweep line algorithm."""
    def __init__(self, x: float, y: float, event_type: int, segment: Segment | list[Segment]):
        self.x = x
        self.y = y
        self.event_type = event_type
        self.segment = segment

    def __repr__(self):
        return f"(segment={self.segment}, type={self.event_type}, point.x {self.x}, point.y {self.y})"

def create_intersection_event(events: list[Event],
                              status,
                              segment1: Segment,
                              segment2: Segment
                              ) -> Event:
    """
    Create an intersection event for two segments at the given x-coordinate.
    The intersection event has the x-coordinate as the intersection point.
    """
    inter = segment1.intersection(segment2)
    if inter:
        events.append(Event(inter.x,
                            inter.y,
                            0,
                            [segment1, segment2]))
        events.sort(key=lambda event: (event.x, event.y, - event.event_type))

        # # Swap the segments in the status list
        # idx1 = status.index(segment1)
        # idx2 = status.index(segment2)
        # status[idx1], status[idx2] = status[idx2], status[idx1]



def insert_sorted(segment, status, event):
    """
    Insert a segment into the status list in sorted order.
    """
    insert_index = 0
    for i, seg in enumerate(status):
        if seg.current_y(event.x) > segment.current_y(event.x):
            insert_index = i
            break
        insert_index = i + 1

    status.insert(insert_index, segment)

def solve(segments: list[Segment]) -> list[Point]:
    """
    Find the intersection points of a set of line segments.
    Use the sweep line algorithm to find the intersections.
    Complexity: O(n log n) where n is the number of segments.
    """
    events = []

    # Add all the start and end points of the segments to the events list
    for _, segment in enumerate(segments):
        if segment.start.x > segment.end.x: # swap if start is greater than end
            segment.start, segment.end = segment.end, segment.start
        events.append(Event(segment.start.x, segment.start.y, 1, segment)) # 1 for start
        events.append(Event(segment.end.x, segment.end.y, -1, segment)) # -1 for end

    events.sort(key=lambda event: (event.x, event.y, - event.event_type))

    # Initialize the sweep line algorithm
    status: list[Segment] = [] # list of segments that are currently intersecting the sweep line
    intersections: set[Point] = set() # list of intersection points

    # Process the events one by one from left to right
    while events:
        event = events.pop(0)
        try:
            segment = event.segment
        except TypeError:
            pass

        if event.event_type == 1:
            insert_sorted(segment, status, event)

            if len(status) > 1:
                # Get index of current segment in status
                idx = status.index(segment)
                if idx > 0:
                    # Compare with below segment
                    create_intersection_event(events, status, status[idx], status[idx - 1])

                if idx < len(status) - 1:
                    # Compare with above segment
                    create_intersection_event(events, status, status[idx], status[idx + 1])

        elif event.event_type == -1:
            # status.sort(key=lambda seg: seg.current_y(event.x)) # sort by current y-coordinate

            # get index of segment in status
            idx = status.index(segment)

            # Compare with the segment above
            if idx > 0:
                create_intersection_event(events, status, segment, status[idx - 1])

            # Compare with the segment below
            if idx < len(status) - 1:
                create_intersection_event(events, status, segment, status[idx + 1])

            # Compare with the remaining segment above and below
            if idx > 0 and idx < len(status) - 1:
                create_intersection_event(events, status, status[idx - 1], status[idx + 1])

            status.remove(segment)

        # if event is an intersection
        else:
            intersections.add(Point(event.x, event.y))
            # Swap the segments in the status list
            segment1, segment2 = event.segment
            try:
                idx1 = status.index(segment1)
                idx2 = status.index(segment2)
                status[idx1], status[idx2] = status[idx2], status[idx1]
            except ValueError:
                continue
                # Mean that the segments have already been removed from the status list

    return intersections

def naive_solve(segments: list[Segment]) -> list[Point]:
    """
    Naive solution to find the intersection points of a set of line segments.
    Compare all pairs of segments to find intersections.
    Complexity: O(n^2) where n is the number of segments.
    """
    intersections = set()
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            inter = segments[i].intersection(segments[j])
            if inter:
                intersections.add(inter)
    return list(intersections)

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

    solve(segments)
