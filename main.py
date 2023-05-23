import sys
import re
import traceback

import core.assets

try:
    from core.common.names import *
    import core.common.resources as cr
    from core.common.functions import *
    from core.assets import *
    from core.controls.shock import Shock
    from core.event_holder import EventHolder

    import asyncio

    pg.init()
    flags = SCALED | FULLSCREEN
    if IS_WEB:
        flags = 0

    cr.screen = make_screen([9,18],25,flags)

    cr.event_holder = EventHolder(cr.screen)

    cr.event_holder.determined_fps = 0

    core.assets.load_assets()




    async def main_loop():
        pic = pics['clown'].copy()
        rotated_pic = pic.copy()
        angle = 0

        shock = Shock()

        while not cr.event_holder.should_quit:
            cr.screen.fill("gray")

            cr.event_holder.get_events()
            shock.check_events()
            # angle += cr.event_holder.dt * 10

            x = shock.finger_angle
            angle = x if x is not None else angle

            rotated_pic = pg.transform.rotate(pic,angle)
            rect = rotated_pic.get_rect()
            rect.center = cr.screen.get_rect().center

            cr.screen.blit(rotated_pic,rect)
            shock.render()

            pg.display.update()
            await asyncio.sleep(0)

    asyncio.run(main_loop())




except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())