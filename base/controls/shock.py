from base.common.names import *
import base.common.resources as cr
from base.common.functions import *


# todo: fix type hinting problems
class Shock:
    def __init__(self, stick_radius=None, container_radius=None):
        if stick_radius is None:
            stick_radius = 7
        if container_radius is None:
            container_radius = stick_radius * 5

        self.container_center: Optional[Vector2] = None
        self.finger_id: Optional[int] = None
        self.finger: Optional[Event] = None

        self.stick_radius = stick_radius
        self.container_radius = container_radius

        self.stick_color = Color("black")
        self.stick_max_color = Color("red")
        self.container_color = Color("black")

    @property
    def normalize_distance(self):
        """
        Normalizes a value between 0 and `radius` to a value between 0 and 1.

        Args:
            radius (float): The upper limit value for normalization.
            value (float): The value to be normalized.

        Returns:
            float: The normalized value between 0 and 1.
        """
        radius = self.container_radius
        value = calculate_distance(self.container_center, self.finger_pos)
        if value <= 0:
            return 0
        elif value >= radius:
            return 1
        else:
            return value / radius

    # bug prone
    @property
    def finger_pos(self) -> Optional[Vector2]:
        if self.container_center is None:
            return None

        return Vector2(self.finger.x, self.finger.y)

    @property
    def collide_points(self):
        res = line_circle_collision_point(
            self.container_center,
            self.container_radius,
            self.container_center,
            self.finger_pos,
        )

        return res

    # bug prone
    @property
    def finger_angle(self) -> Optional[float]:
        if self.container_center is None:
            return None

        v1 = Vector2(0, 0)
        v2 = Vector2(
            self.finger_pos.x - self.container_center.x,
            self.finger_pos.y - self.container_center.y,
        )

        return v2.angle_to(v1) - 90

    def check_events(self):
        if self.container_center is None:
            # listen to finger taps
            # and fill pillar_center and finger data
            for tap_id in cr.event_holder.tapped_fingers:
                if tap_id in cr.event_holder.fingers:
                    self.finger_id = tap_id
                    self.finger = cr.event_holder.fingers[tap_id]
                    self.container_center = Vector2(self.finger.x, self.finger.y)
                    break
        else:
            # listen to finger positional updates
            for hold_id in cr.event_holder.held_fingers:
                if hold_id == self.finger_id and hold_id in cr.event_holder.fingers:
                    self.finger = cr.event_holder.fingers[hold_id]

            # listen to finger lifts
            # and clear pillar_center and finger data
            for lift_id in cr.event_holder.lifted_fingers:
                if lift_id == self.finger_id:
                    self.finger_id = None
                    self.finger = None
                    self.container_center = None
                    break

    def render(self):
        if self.container_center is not None:
            collide_points = self.collide_points
            # print(type(c))
            color = self.stick_color
            overstep = True
            if point_in_circle(
                self.finger_pos, self.container_center, self.container_radius
            ):
                color = "blue"
                overstep = False

                # print(type(i),type(d),i,d)
                # pg.draw.line(cr.screen,"black",Vector2(i[0],i[1]),Vector2(d[0],d[1]),width=1)

            if len(collide_points):
                pg.draw.circle(cr.screen, color, collide_points[0], 3)

            finger_pos = self.finger_pos
            if overstep and len(collide_points):
                finger_pos = collide_points[0]

            stick_color = self.stick_color.lerp(
                self.stick_max_color, self.normalize_distance
            )

            pg.draw.circle(cr.screen, stick_color, finger_pos, self.stick_radius)
            pg.draw.circle(
                cr.screen,
                self.container_color,
                self.container_center,
                self.container_radius,
                width=3,
            )
