from core.common.names import *
import core.common.resources as cr
from core.assets import *
from core.controls.spectrum import Spectrum
from core.controls.shock import Shock

class Test:
    def __init__(self):
        self.pic = pics['clown'].copy()
        self.rotated_pic = self.pic.copy()
        self.angle = 0

        self.use_shock = False
        self.shock = Shock()
        self.spectrum = Spectrum()

    def check_events( self ):
        if cr.event_holder.mouse_pressed_keys[2] or (len(cr.event_holder.fingers) > 1
                                and len(cr.event_holder.tapped_fingers)):
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