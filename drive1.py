import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
import keyboard

from helper_keyboard_input import KeyboardHelper
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync

# initialize global variables
current_key_code = -1
driving_keys = [119, 97, 115, 100, 32]
speed = 0
heading = 0
flags = 0

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

def keycode_callback(keycode):
    global current_key_code
    current_key_code = keycode
    print("Key code updated: ", str(current_key_code))

def key_commands(self, e):
    if str(e) == 'KeyboardEvent(w down)':
      print("Got key release event: " + str(e))
      speed = 65
      flag = 0

async def main():
    """
    Runs the main control loop for this demo.  Uses the KeyboardHelper class to read a keypress from the terminal.
    W - Go forward.  Press multiple times to increase speed.
    A - Decrease heading by -10 degrees with each key press.
    S - Go reverse. Press multiple times to increase speed.
    D - Increase heading by +10 degrees with each key press.
    Spacebar - Reset speed and flags to 0. RVR will coast to a stop
    """
    global current_key_code
    global speed
    global heading
    global flags

    await rvr.wake()

    await rvr.reset_yaw()

    print("Sphero team sux at python")

    while True:

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        # check the heading value, and wrap as necessary.
        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        # reset the key code every loop
        current_key_code = -1

        # issue the driving command
        await rvr.drive_with_heading(speed, heading, flags)

        # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
        await asyncio.sleep(0.1)


def run_loop():
    global loop
    keyboard.hook(self.key_command)    
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )

if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
    finally:
        print("Press any key to exit.")
        exit(1)
