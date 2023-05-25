from base.common.names import *
import base.common.resources as cr
from base.assets import *
from base.controls.spectrum import Spectrum
from base.controls.shock import Shock

class Test:
    def __init__(self):
        self.pic = base_pics['clown'].copy()
        self.rotated_pic = self.pic.copy()
        self.angle = 0

        self.use_shock = False
        self.shock = Shock()
        self.spectrum = Spectrum(Vector2(1,0.1))

    # done: fix the EventHolder.fingers mouse conflict
    def check_events( self ):
        held_fingers = [i for i in cr.event_holder.held_fingers if i != -1]
        tapped_fingers = [i for i in cr.event_holder.tapped_fingers if i != -1]

        if cr.event_holder.mouse_pressed_keys[2] or (len(held_fingers) > 1 and len(tapped_fingers)!=0):
            self.use_shock = not self.use_shock

        if self.use_shock:
            self.shock.check_events()

            x = self.shock.finger_angle
            self.angle = x if x is not None else self.angle

            self.rotated_pic = pg.transform.rotate(self.pic, self.angle)

        else:
            self.spectrum.check_events()

            x = self.spectrum.angle

            if x is None:
                self.spectrum.angle_anchor = self.angle
            else:
                self.angle = x

            self.rotated_pic = pg.transform.rotate(self.pic, self.angle)

    def render( self ):
        rect = self.rotated_pic.get_rect()
        rect.center = cr.screen.get_rect().center

        cr.screen.blit(self.rotated_pic, rect)

        if self.use_shock:
            self.shock.render()
        else:
            self.spectrum.render()