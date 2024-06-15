import matplotlib.pyplot as plt
import heapq
from sortedcontainers import SortedList


class Point:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def format_point(self) -> str:
        """Return the point in the format (x, y)."""
        return f"(axis cs:{self.x}, {self.y})"
    
    def format_point_segment_pgf(self) -> str:
        """Return the point in the format x y."""
        return f"({self.x}, {self.y})"

class Segment:
    def __init__(self, p1, p2):
        if p1 < p2:
            self.start: Point = p1
            self.end: Point = p2
        else:
            self.start: Point = p2
            self.end: Point = p1

    def __eq__(self, other):
        if isinstance(other, Segment):
            return self.start == other.start and self.end == other.end
        return False

    def __repr__(self):
        return f"Segment({self.start}, {self.end})"

    def __lt__(self, other):
        # Compare segments based on their y-coordinates at the current x-coordinate
        if self.start.x == other.start.x:
            return self.start.y < other.start.y
        return self.start.x < other.start.x

    def segment_to_pgf(self) -> str:
        """Return the segment in the PGFPlots format."""
        return f"\\addplot[red, mark=*] coordinates {{{self.start.format_point_segment_pgf()} {self.end.format_point_segment_pgf()}}};"

    def compute_y(self, x):
        """ Compute the y-coordinate of the segment at the given x-coordinate """
        if self.start.x == self.end.x:
            return self.start.y
        slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        return self.start.y + slope * (x - self.start.x)

    def segment_key(self, x):
        """ Return the y-coordinate of the segment at the given x-coordinate """
        return self.compute_y(x)

class Event:
    def __init__(self,
                 point: Point,
                 segment: Segment,
                 event_type: str,
                 intersection_segments: list[Segment] = None
                 ) -> None:
        """ Create an event object """
        self.point: Point = point
        self.segment: Segment = segment
        self.event_type: str = event_type  # "start", "end", or "intersection"
        self.intersection_segments: list[Segment] = []

    def __lt__(self, other):
        # Compare by x coordinate first
        if self.point.x != other.point.x:
            return self.point.x < other.point.x
        # If x coordinates are the same, compare by event type priority
        event_priority = {"start": 0, "intersection": 1, "end": 2}
        if self.event_type != other.event_type:
            return event_priority[self.event_type] < event_priority[other.event_type]
        # If event types are the same, compare by y coordinate to maintain a consistent order
        return self.point.y < other.point.y

    def __repr__(self):
        return f"Event({self.point}, {self.segment}, {self.event_type})"

def segment_intersection(segment1: Segment, segment2: Segment) -> Point | bool:
    """ Check if two segments intersect """
    x1, y1 = segment1.start.x, segment1.start.y
    x2, y2 = segment1.end.x, segment1.end.y
    x3, y3 = segment2.start.x, segment2.start.y
    x4, y4 = segment2.end.x, segment2.end.y

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

def swap_elements(sorted_list, idx1, idx2):
    """ Swap two elements in a sorted list"""
    if idx1 >= len(sorted_list) or idx2 >= len(sorted_list):
        raise IndexError("Index out of range")

    # Remove the elements at idx1 and idx2
    segment1 = sorted_list.pop(idx1)
        # Adjust idx2 if it follows idx1
    segment2 = sorted_list.pop(idx2 - 1 if idx2 > idx1 else idx2)

    # Swap and re-add them
    sorted_list.add(segment1)
    sorted_list.add(segment2)

def solve(segments: list[Segment]) -> list[Point]:
    events: list[Event] = []
    for segment in segments:
        events.append(Event(segment.start, segment, "start"))
        events.append(Event(segment.end, segment, "end"))

    heapq.heapify(events)


#     x_event = min(events, key=lambda event: event.point.x).point.x

    active_segments: SortedList[Segment] = SortedList()
    intersections = []

    def add_segment(segment):
        active_segments.add(segment)

    def remove_segment(segment):
        active_segments.remove(segment)

    def find_intersections(seg, events):
        idx = active_segments.index(seg)
        if idx > 0:
            pred = active_segments[idx - 1]
            ip = segment_intersection(seg, pred)
            if ip:
                intersections.append(ip)
                heapq.heappush(events, Event(ip, None, "intersection", [seg, pred]))
        if idx < len(active_segments) - 1:
            succ = active_segments[idx + 1]
            ip = segment_intersection(seg, succ)
            if ip:
                intersections.append(ip)
                heapq.heappush(events, Event(ip, None, "intersection", [seg, succ]))

    

    while events:
        event = heapq.heappop(events)
        print(event)
        x_event = event.point.x
        if event.event_type == "start":
            add_segment(event.segment)
            # Check for intersections with the previous and next segments
            find_intersections(event.segment, events)

        elif event.event_type == "end":
            idx = active_segments.index(event.segment)

            # Check for intersections with the previous and next segments
            find_intersections(event.segment, events)

            # Check for intersections between the previous and next segments
            if idx > 0 and idx < len(active_segments) - 1:
                ip = segment_intersection(active_segments[idx - 1],
                                          active_segments[idx + 1])
                if ip:
                    intersections.append(ip)
                    heapq.heappush(events, Event(ip, None, "intersection"))
            remove_segment(event.segment)

        elif event.event_type == "intersection":
            try:
                idx1 = active_segments.index(event.intersection_segments[0])
                idx2 = active_segments.index(event.intersection_segments[1])
            except IndexError:
                continue
            swap_elements(active_segments, idx1, idx2)
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
            inter = segment_intersection(segments[i], segments[j])
            if inter:
                intersections.add(inter)
    return list(intersections)

if __name__ == "__main__":
    # Example
    segments = [
        Segment(Point(1, 1), Point(4, 4)),
        # Segment(Point(1, 3), Point(3, 1)),
        # Segment(Point(3, 1), Point(5, 3)),
        # Segment(Point(3, 2), Point(5, 0)),
        # Segment(Point(2, 1), Point(2.6, 1.5)),
        Segment(Point(3, 4), Point(5, 2)),
        Segment(Point(3, 3.5), Point(4.5, 1.5)),
        # Segment(Point(3.5, 2), Point(4.5, 3.5)),
        # Segment(Point(2.5, 3), Point(3.5, 2.5)),
        # Segment(Point(3, 2.5), Point(4, 3.5)),
        # Segment(Point(1.5, 4), Point(1.75, 0))
    ]

    intersections = solve(segments)
    print(intersections)