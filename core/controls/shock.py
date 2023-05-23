from core.common.names import *
import core.common.resources as cr
from core.common.functions import *
from core.assets import *


class Shock :

    def __init__( self ) :
        self.pillar_center: Optional[Vector2] = None
        self.finger_id: Optional[int] = None
        self.finger: Optional[Event] = None

        self.stick_radius = 7
        self.container_radius = self.stick_radius * 5

        self.stick_color = Color("red")
        self.container_color = Color("black")


    # bug prone
    @property
    def finger_pos( self ) -> Optional[Vector2] :
        if self.pillar_center is None :
            return None

        return Vector2(self.finger.x, self.finger.y)


    @property
    def collide_points( self ) :
        res = line_circle_collision_point(
            self.pillar_center,
            self.container_radius,
            self.pillar_center,
            self.finger_pos)

        return res


    # bug prone
    @property
    def finger_angle( self ) -> Optional[float] :
        if self.pillar_center is None :
            return None

        v1 = Vector2(0, 0)
        v2 = Vector2(self.finger_pos.x - self.pillar_center.x,
            self.finger_pos.y - self.pillar_center.y)

        return v2.angle_to(v1) - 90


    def check_events( self ) :
        if self.pillar_center is None :
            # listen to finger taps
            # and fill pillar_center and finger data
            for tap_id in cr.event_holder.tapped_fingers :
                if tap_id in cr.event_holder.fingers :
                    self.finger_id = tap_id
                    self.finger = cr.event_holder.fingers[tap_id]
                    self.pillar_center = Vector2(self.finger.x, self.finger.y)
                    break
        else :
            # listen to finger positional updates
            for hold_id in cr.event_holder.held_fingers :
                if hold_id == self.finger_id and hold_id in cr.event_holder.fingers :
                    self.finger = cr.event_holder.fingers[hold_id]

            # listen to finger lifts
            # and clear pillar_center and finger data
            for lift_id in cr.event_holder.lifted_fingers :
                if lift_id == self.finger_id :
                    self.finger_id = None
                    self.finger = None
                    self.pillar_center = None
                    break


    def render( self ) :
        if self.pillar_center is not None :
            c = self.collide_points
            # print(type(c))
            for i in c:
                # print(type(i),type(d),i,d)
                # pg.draw.line(cr.screen,"black",Vector2(i[0],i[1]),Vector2(d[0],d[1]),width=1)
                pg.draw.circle(cr.screen, self.stick_color, i, 3)

            pg.draw.circle(cr.screen, self.stick_color, self.finger_pos, self.stick_radius)
            pg.draw.circle(cr.screen, self.container_color, self.pillar_center,
                self.container_radius, width=3)
