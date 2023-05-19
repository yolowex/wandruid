from core.common.names import *

def make_screen(aspect_ratio,scale,flags=None) -> Surface:
    ar = aspect_ratio
    return pg.display.set_mode([ar[0]*scale,ar[1]*scale],flags)
