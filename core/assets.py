from core.common.names import *
from core.common.constants import *

pics: Dict[str,Surface] = {}

def load_assets():
    pics['clown'] = pg.image.load(here+"assets/clown.png")
    pics['boat'] = pg.image.load(here+"assets/boat.png")
    pics['honey'] = pg.image.load(here+"assets/honey.png")
