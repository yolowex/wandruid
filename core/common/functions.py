from core.common.names import *

def make_screen(aspect_ratio,scale,flags=None) -> Surface:
    ar = aspect_ratio
    return pg.display.set_mode([ar[0]*scale,ar[1]*scale],flags)


def line_circle_collision_point(circle_center:Vector2, circle_radius, point_a:Vector2, point_b:Vector2):
    # Create symbolic variables
    x, y = symbols('x y')

    # Define equation for the circle
    circle_eq = Eq((x - circle_center[0])**2 + (y - circle_center[1])**2, circle_radius**2)

    # Define equation for the line
    line_eq = Eq((point_b.y - point_a.y) * x - (point_b.x - point_a.x) * y +
                 point_b.x * point_a.y - point_b.y * point_a.x, 0)

    # Solve the equations to find intersection points
    collision_points = solve((circle_eq, line_eq), (x, y))
    print(collision_points)

    return collision_points