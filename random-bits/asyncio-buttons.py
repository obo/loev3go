#!/usr/bin/env python3
# needs python 35
# from http://python-evdev.readthedocs.io/en/latest/tutorial.html

import asyncio, evdev

mouse = evdev.InputDevice('/dev/input/event4')
#keybd = evdev.InputDevice('/dev/input/event5')
camerabutton = evdev.InputDevice('/dev/input/by-id/usb-SunplusIT_Inc_Integrated_Camera-event-if00')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')

for device in mouse, camerabutton: #mouse, keybd:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
