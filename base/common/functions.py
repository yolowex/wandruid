from base.common.names import *


def now():
    return pg.time.get_ticks() / 1000


def make_screen(aspect_ratio, scale, flags=None) -> Surface:
    ar = aspect_ratio
    return pg.display.set_mode([ar[0] * scale, ar[1] * scale], flags)


def line_circle_collision_point(circle_center, circle_radius, line_start, line_end):
    # def line_circle_collision( line_start, line_end, circle_center, circle_radius ) :
    """
    Calculates the collision points between a line and a circle.

    Args:
        line_start (tuple): Coordinates of the line's starting point (x, y).
        line_end (tuple): Coordinates of the line's ending point (x, y).
        circle_center (tuple): Coordinates of the circle's center (x, y).
        circle_radius (float): Radius of the circle.

    Returns:
        list: A list of collision points, where each point is represented by a tuple (x, y).
    """
    start = np.array(line_start)
    end = np.array(line_end)
    center = np.array(circle_center)

    # Vector representing the line segment
    line_vector = end - start

    # Vector from the line's starting point to the circle's center
    start_to_center = center - start

    # Calculate the projection of start_to_center onto the line_vector
    projection = np.dot(start_to_center, line_vector) / np.dot(line_vector, line_vector)

    # Find the closest point on the line segment to the circle's center
    closest_point = start + projection * line_vector

    # Calculate the distance between the closest point and the circle's center
    distance = np.linalg.norm(closest_point - center)

    # Check if the closest point lies within the line segment
    if 0 <= projection <= 1:
        # Check if the distance is less than or equal to the circle's radius
        if distance <= circle_radius:
            # Calculate the collision points
            direction = line_vector / np.linalg.norm(line_vector)
            collision1 = closest_point + direction * (circle_radius - distance)
            collision2 = closest_point - direction * (circle_radius - distance)
            return [tuple(collision1)]

    return []  # No collision points found


def point_in_circle(point, circle_center, circle_radius):
    """
    Determines if a point is inside a circle.

    Args:
        point (tuple): Coordinates of the point (x, y).
        circle_center (tuple): Coordinates of the circle's center (x, y).
        circle_radius (float): Radius of the circle.

    Returns:
        bool: True if the point is inside the circle, False otherwise.
    """
    # Calculate the distance between the point and the circle's center
    distance = math.sqrt(
        (point[0] - circle_center[0]) ** 2 + (point[1] - circle_center[1]) ** 2
    )

    # Check if the distance is less than or equal to the circle's radius
    if distance <= circle_radius:
        return True
    else:
        return False


import math


def calculate_distance(point1, point2):
    """
    Calculates the distance between two points in 2D space.

    Args:
        point1 (tuple): Coordinates of the first point (x1, y1).
        point2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
        float: The distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance
