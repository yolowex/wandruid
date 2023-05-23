import sys
import re
import traceback

from base.controls.spectrum import Spectrum
from base.test import Test

try:
    from base.common.names import *
    import base.assets
    import base.common.resources as cr
    from base.common.functions import *
    from base.assets import *
    from base.controls.shock import Shock
    from base.event_holder import EventHolder

    from gui.menu import Menu
    from gui.drawables.page import Page


    import asyncio

    pg.init()
    flags = SCALED | FULLSCREEN
    if IS_WEB:
        flags = 0

    cr.screen = make_screen([9,18],25,flags)

    cr.event_holder = EventHolder(cr.screen)

    cr.event_holder.determined_fps = 0

    menu = Menu(cr.screen,cr.event_holder)

    base.assets.load_assets()


    test = Test()




    async def main_loop():


        while not cr.event_holder.should_quit:
            cr.screen.fill("gray")

            cr.event_holder.get_events()

            test.check_events()
            test.render()


            pg.display.update()
            await asyncio.sleep(0)

    asyncio.run(main_loop())




except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())