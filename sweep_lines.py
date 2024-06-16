#!/usr/bin/env python3
"""
A Python implementation of the sweep line algorithm
to find the intersection points of a set of line segments.
"""
import heapq
from sortedcontainers import SortedList


class Point:
    """A class to represent a point in 2D space."""
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

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
    """A class to represent a line segment."""
    def __init__(self, p1, p2):
        if p1 < p2:
            self.start: Point = p1
            self.end: Point = p2
        else:
            self.start: Point = p2
            self.end: Point = p1

    def __eq__(self, other):
        """Check if two segments are equal."""
        if isinstance(other, Segment):
            return self.start == other.start and self.end == other.end
        return False

    def __repr__(self):
        """Return a string representation of the segment."""
        return f"Segment({self.start}, {self.end})"

    def __lt__(self, other):
        """Compare two segments based on their y-coordinates at the current x-coordinate."""
        if self.start.x == other.start.x:
            return self.start.y < other.start.y
        return self.start.x < other.start.x

    def segment_to_pgf(self) -> str:
        """Return the segment in the PGFPlots format."""
        return f"\\addplot[red, mark=*] coordinates {{{self.start.format_point_segment_pgf()} {self.end.format_point_segment_pgf()}}};"

    def current_y(self, x):
        """ Compute the y-coordinate of the segment at the given x-coordinate """
        if self.start.x == self.end.x:
            return self.start.y
        slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        return self.start.y + slope * (x - self.start.x)

class Event:
    """ A class to represent an event in the sweep line algorithm."""
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
        self.intersection_segments: list[Segment] = intersection_segments

    def __lt__(self, other):
        """
        Compare two events based on their x-coordinate,
        event type, and y-coordinate.
        """
        if self.point.x != other.point.x:
            return self.point.x < other.point.x

        event_priority = {"start": 2, "intersection": 1, "end": 0}
        if self.event_type != other.event_type:
            return event_priority[self.event_type] < event_priority[other.event_type]

        return self.point.y < other.point.y

    def __repr__(self):
        """ Return a string representation of the event."""
        return f"Event({self.point}, {self.segment}, {self.event_type}, {self.intersection_segments})"

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

        return Point(round(intersection_x, 5), round(intersection_y, 5))
    return False


def add_segment(event: list[Event], active_segments: list[Segment]):
    def insert_sorted(segment: Segment,
                    status: list[Segment],
                    x: float
                    ) -> None:
        """
        Insert a segment into the status list in sorted order.
        """
        insert_index = 0
        for i, seg in enumerate(status):
            if seg.current_y(x) > segment.current_y(x):
                insert_index = i
                break
            insert_index = i + 1

        status.insert(insert_index, segment)
    x = event.point.x
    segment = event.segment
    insert_sorted(segment, active_segments, x)

def remove_segment(segment, active_segments: list[Segment]):
    active_segments.remove(segment)

def solve(segments: list[Segment]) -> list[Point]:
    """ Main function to solve the intersection problem using the sweep line algorithm."""
    events: list[Event] = []
    for segment in segments:
        events.append(Event(segment.start, segment, "start"))
        events.append(Event(segment.end, segment, "end"))

    heapq.heapify(events)

    active_segments: list[Segment] = []
    intersections = set()

    def find_intersections(seg, events):
        idx = active_segments.index(seg)
        if idx > 0:
            pred = active_segments[idx - 1]
            ip = segment_intersection(seg, pred)
            if ip and not ip in intersections:
                intersections.add(ip)
                heapq.heappush(events, Event(ip, None, "intersection", [seg, pred]))
        if idx < len(active_segments) - 1:
            succ = active_segments[idx + 1]
            ip = segment_intersection(seg, succ)
            if ip and not ip in intersections:
                intersections.add(ip)
                heapq.heappush(events, Event(ip, None, "intersection", [seg, succ]))

    def swap_segments(status: list[Segment],
                    intersection_segments: list[Segment]
                    ) -> bool:
        """
        Swap the positions of two segments in the status list.
        Return True if the segments are swapped, otherwise False.
        """
        
        def upper_shift(status_segments, idx1, idx2):
            sub_status_segments = status_segments[idx1:idx2+1]
            premier = sub_status_segments.pop(0)
            sub_status_segments.append(premier)
            status_segments[idx1:idx2+1] = sub_status_segments

        if len(intersection_segments) != 2:
            return

        segment1, segment2 = intersection_segments

        if segment1 not in status or segment2 not in status:
            return

        idx1 = status.index(segment1)
        idx2 = status.index(segment2)

        if segment1.start.y >= segment2.start.y:
            if idx1 > idx2:
                # status[idx1], status[idx2] = status[idx2], status[idx1]
                upper_shift(status, idx2, idx1)
                # Check for intersections with the previous and next segments
                find_intersections(segment1, events)
                find_intersections(segment2, events)
                return True
        else:
            if idx1 < idx2:
                # status[idx1], status[idx2] = status[idx2], status[idx1]
                upper_shift(status, idx1, idx2)
                # Check for intersections with the previous and next segments
                find_intersections(segment1, events)
                find_intersections(segment2, events)
                return True
        return False

    while events:
        event = heapq.heappop(events)

        if event.event_type == "start":
            add_segment(event, active_segments)
            # Check for intersections with the previous and next segments
            find_intersections(event.segment, events)

        elif event.event_type == "end":
            idx = active_segments.index(event.segment)

            # Check for intersections with the previous and next segments
            find_intersections(event.segment, events)

            # Check for intersections between the previous and next segments
            if idx > 0 and idx < len(active_segments) - 1:
                pred = active_segments[idx - 1]
                succ = active_segments[idx + 1]
                ip = segment_intersection(active_segments[idx - 1],
                                          active_segments[idx + 1])
                if ip and not ip in intersections:
                    intersections.add(ip)
                    heapq.heappush(events, Event(ip, None, "intersection", [pred, succ]))
            remove_segment(event.segment, active_segments)

        elif event.event_type == "intersection":
            swap_segments(active_segments, event.intersection_segments)    

    return list(intersections)

def semi_naive_solve(segments: list[Segment]) -> list[Point]:
    """
    Semi-naive solution to find the intersection points of a set of line segments.
    Compare all pairs of active segments to find intersections.
    """
    events: list[Event] = []
    for segment in segments:
        events.append(Event(segment.start, segment, "start"))
        events.append(Event(segment.end, segment, "end"))

    heapq.heapify(events)

    active_segments: list[Segment] = []
    intersections = set()

    while events:
        event = heapq.heappop(events)

        if event.event_type == "start":
            add_segment(event, active_segments)

        elif event.event_type == "end":
            idx = active_segments.index(event.segment)

            for i, active_segment in enumerate(active_segments):
                if i != idx:
                    inter = segment_intersection(event.segment, active_segment)
                    if inter and not inter in intersections:
                        intersections.add(inter)

            remove_segment(event.segment, active_segments)
    return list(intersections)



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
            if inter and not inter in intersections:
                intersections.add(inter)
    return list(intersections)
