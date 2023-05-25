from base.common.names import *
from base.common.constants import *

base_pics: Dict[str,Surface] = {}
base_fonts: Dict[str,Font] = {}

def load_assets():
    base_pics['clown'] = pg.image.load(here+"assets/clown.png")


    base_fonts['big'] = SysFont('Arial',30)

