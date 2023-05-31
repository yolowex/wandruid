from base.common.names import *
import base.common.resources as cr
from base.common.functions import *


class Spectrum:
    def __init__(self, container_size_scale: Vector2):
        self.pillar_center: Optional[Vector2] = None
        self.container_size: Vector2 = Vector2(
            cr.screen.get_width() * container_size_scale.x,
            cr.screen.get_height() * container_size_scale.y,
        )
        self.container_center: Optional[Vector2] = None
        self.finger_id: Optional[int] = None
        self.finger: Optional[Event] = None

        self.angle_anchor = 0
        self.angle_wideness = 180
        self.stick_radius = 7
        self.stick_color = Color("black")
        self.stick_min_color = Color("blue")
        self.stick_max_color = Color("red")
        self.container_color = Color("black")

    @property
    def angle(self):
        x = self.value
        return (
            (x * -abs(self.angle_wideness)) + self.angle_anchor
            if x is not None
            else None
        )

    @property
    def finger_pos(self) -> Optional[Vector2]:
        if self.container_center is None:
            return None

        return Vector2(self.finger.x, self.container_center.y)

    @property
    def value(self):
        if self.container_center is None:
            return None

        return self.normalize_distance

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
        radius = self.container_size.x / 2
        value = calculate_distance(self.container_center, self.finger_pos)
        m = -1 if self.finger_pos.x < self.container_center[0] else 1
        if value <= 0:
            return 0
        elif value >= radius:
            return m
        else:
            return value / radius * m

    def check_events(self):
        if self.container_center is None:
            # listen to finger taps
            # and fill pillar_center and finger data
            for tap_id in cr.event_holder.tapped_fingers:
                if tap_id in cr.event_holder.fingers:
                    self.finger_id = tap_id
                    self.finger = cr.event_holder.fingers[tap_id]

                    if self.pillar_center is None:
                        self.container_center = Vector2(self.finger.x, self.finger.y)
                    else:
                        self.container_center = Vector2(self.pillar_center)
                    break
        else:
            if self.pillar_center is not None:
                self.container_center = Vector2(self.pillar_center)
            # listen to finger movements
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
        if not cr.event_holder.should_render_debug:
            return

        if self.container_center is not None:
            rect = Rect(0, 0, self.container_size.x, self.container_size.y)
            rect.center = self.container_center
            finger_pos = self.finger_pos
            left = finger_pos.x < rect.center[0]

            if not rect.collidepoint(finger_pos):
                if left:
                    finger_pos.x = rect.x
                else:
                    finger_pos.x = rect.x + rect.w

            target_color = self.stick_max_color
            if left:
                target_color = self.stick_min_color

            stick_color = self.stick_color.lerp(
                target_color, abs(self.normalize_distance)
            )

            pg.draw.circle(cr.screen, stick_color, finger_pos, self.stick_radius)
            pg.draw.rect(cr.screen, self.container_color, rect, width=3)
