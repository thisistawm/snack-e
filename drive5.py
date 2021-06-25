import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
import keyboard
import signal
import time
import traceback

from helper_keyboard_input import KeyboardHelper
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync

# initialize global variables
key_helper = KeyboardHelper()
current_key_code = -1
driving_keys = [119, 97, 115, 100, 32]
speed = 0
heading = 0
flags = 0

speedVar = 0
headingVar = 0
flagsVar = 0

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

def my_on_key_event(e):
    global speedVar
    global headingVar
    global flagsVar

    print("Got key release event: " + str(e))
    if str(e) == 'KeyboardEvent(w down)':
        speedVar = 65
        flagsVar = 0
        print ('w pressed:' + str(speedVar))
    if str(e) == 'KeyboardEvent(w up)':
        speedVar = 0

    if str(e) == 'KeyboardEvent(s down)':
        speedVar = 65
        flagsVar = 1

    if str(e) == 'KeyboardEvent(s up)':
        speedVar = 0

    if str(e) == 'KeyboardEvent(a down)':
        headingVar -= 10

    # if str(e) == 'KeyboardEvent(a up)':
        # headingVar = 0

    if str(e) == 'KeyboardEvent(d down)':
        headingVar += 10

    # if str(e) == 'KeyboardEvent(d up)':
        # headingVar = 0


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
    global speedVar
    global headingVar
    global flagsVar

    keyboard.hook(my_on_key_event)

    await rvr.wake()

    await rvr.reset_yaw()

    while True:

        speed = speedVar
        print("speed set to: " + str(speed) + " // speedVar set to: " + str(speedVar))
        heading = headingVar
        flags = flagsVar

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
    global key_helper
    key_helper.set_callback(keycode_callback)
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )


if __name__ == "__main__":
    loop.run_in_executor(None, key_helper.get_key_continuous)
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        key_helper.end_get_key_continuous()
    except IOError as err:
        print ("I/O error")
    except ValueError:
        print ("Could not convert data to an integer.")
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        traceback.print_exc()
        print("Press any key to exit.")
        exit(1)
