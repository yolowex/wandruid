from core.common.names import *
import core.common.resources as cr


class Shock :

    def __init__( self ) :
        self.pillar_center: Optional[Vector2] = None
        self.finger_id: Optional[int] = None
        self.finger: Optional[Event] = None

        self.stick_radius = 5
        self.container_radius = self.stick_radius * 2.5

        self.stick_color = Color("red")
        self.container_color = Color("black")


    def check_events( self ) :
        if self.pillar_center is None :
            # listen to finger taps
            # and fill pillar_center and finger data
            for tap_id in cr.event_holder.tapped_fingers :
                if tap_id in cr.event_holder.fingers :
                    self.finger_id = tap_id
                    self.finger = cr.event_holder.fingers[tap_id]
                    self.pillar_center = self.finger.x, self.finger.y
                    break
        else :
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
            pg.draw.circle(cr.screen, self.stick_color, self.pillar_center, self.stick_radius)
            pg.draw.circle(cr.screen, self.container_color, self.pillar_center,
                self.container_radius, width=3)
