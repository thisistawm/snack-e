import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
import keyboard
import signal
import sched, time
import traceback
import inputs
from datetime import datetime

from multiprocessing import Process

from helper_keyboard_input import KeyboardHelper
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync

from threading import Thread

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

eventCode = ""
headingFlag = ""
danceFlag = ""
turboFlag = False

breakFlag = False

statusCheckReps = 0
lonelyTimer = 0

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
    global eventCode
    global headingFlag
    global danceFlag

    x = 0
    danceReps = 0

    await rvr.wake()

    await rvr.reset_yaw()

    def gamepad():
        global breakFlag
        global eventCode
        global speedVar
        global headingVar
        global flagsVar
        global headingFlag
        global danceFlag
        global turboFlag
        global lonelyTimer

        while breakFlag==False:
            events = inputs.get_gamepad()
            for event in events:
                #print("w00t")
                eventCode = (str(event.code) + str(event.state))

            if "ABS_Y0" in eventCode:
                speedVar = 65
                flagsVar = 0
                print("forward")
                lonelyTimer = 0

            if "ABS_Y128" in eventCode:
                speedVar = 0
                lonelyTimer = 0

            if "ABS_Y255" in eventCode:
                speedVar = 65
                flagsVar = 1
                print("backward")
                lonelyTimer = 0

            if "ABS_X0" in eventCode:
                headingVar -= 10
                headingFlag = "left"
                print("left")
                lonelyTimer = 0

            if "ABS_X128" in eventCode:
                headingFlag = "center"
                lonelyTimer = 0

            if "ABS_X255" in eventCode:
                headingVar += 10
                headingFlag = "right"
                print("right")
                lonelyTimer = 0

            if "BTN_EAST1" in eventCode:
                headingFlag = "center"
                speedVar = 0
                flagsVar = 0
                danceFlag = "A"
                print("spin")
                lonelyTimer = 0

            if "BTN_C1" in eventCode:
                headingFlag = "center"
                speedVar = 0
                flagsVar = 0
                danceFlag = "B"
                print("wiggle")
                lonelyTimer = 0

            if "BTN_NORTH1" in eventCode:
                headingFlag = "center"
                speedVar = 0          
                flagsVar = 0
                danceFlag = "Y"
                print("twerk")
                lonelyTimer = 0

            if "BTN_SOUTH1" in eventCode:
                headingFlag = "center"
                speedVar = 0          
                flagsVar = 0 
                danceFlag = "X"
                print("cowboy")
                lonelyTimer = 0

            if "BTN_TR21" in eventCode:
                headingFlag = "center"
                speedVar = 0          
                flagsVar = 0
                danceFlag = "START"
                print("wake up")
                lonelyTimer = 0

            if "BTN_TL21" in eventCode:
                headingFlag = "center"
                speedVar = 0          
                flagsVar = 0
                danceFlag = "SELECT"
                print("turn around")
                lonelyTimer = 0

            if "BTN_Z1" in eventCode:
                turboFlag = True
                print("TURBO ON")
                lonelyTimer = 0

            if "BTN_Z0" in eventCode:  
                turboFlag = False
                print("TURBO OFF")
                lonelyTimer = 0  

            if "BTN_WEST1" in eventCode:
                danceFlag = "L"
                lonelyTimer = 0
        return

    gamepad = Thread(target = gamepad)
    gamepad.start()

    def statusCheck():        
        global breakFlag
        while breakFlag==False:
          global statusCheckReps
          global lonelyTimer
          statusCheckReps+=1
          lonelyTimer+=1
          now = datetime.now()     
          print("The time is", now)
          print("Snack-E has been alive for " + str(statusCheckReps) + " status checks")
          print("")
          #def lonelySound():      
          #    os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/lonely-small.mp3")
          #    return
          #lonelySoundThread = Thread(target = lonelySound)
          #if lonelyTimer > 20:
          #    lonelySoundThread.start() 
          #    loneylyTime = 0
          #    time.sleep(10)
          time.sleep(60)  
        return

    
    #statusCheck = Thread(target = statusCheck)
    #statusCheck.start() 

    while True:
        
        if danceFlag == "A":
            print("DANCE")

        x += 1
        #print ("loop: " + str(eventCode))


        # check the heading value, and wrap as necessary.
        if headingVar > 359:
            headingVar = headingVar - 359
        elif headingVar < 0:
            headingVar = 359 + headingVar

        if headingFlag == "left":
            if headingVar >= 10:
                headingVar -= 10
        elif headingFlag == "right":
            if headingVar <= 349:
                headingVar += 10

        speed = speedVar
        if turboFlag and speedVar>0:
          speedVar = 160
        if turboFlag==False and speedVar>0:
          speedVar = 65
        heading = headingVar
        flags = flagsVar

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        # issue the driving command
        await rvr.drive_with_heading(speed, heading, flags)
 
       # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.            
        await asyncio.sleep(0.1)

        if danceFlag == "A":
            #await rvr.drive_with_heading(speed=0,heading=50,flags=0)
            #await asyncio.sleep(0.1)

            def aSound():      
                os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/a-spin-small.mp3")
                return

            aSoundThread = Thread(target = aSound)
            aSoundThread.start()  

            await asyncio.sleep(2)
            await rvr.raw_motors(1, 200, 2, 200)
            await asyncio.sleep(2)
            await rvr.raw_motors(1, 200, 2, 200)
            await asyncio.sleep(1)
            await asyncio.sleep(2) 
            danceReps = 0
            danceFlag = ""

        if danceFlag == "B":
            #await rvr.drive_with_heading(speed=0,heading=50,flags=0)
            #await asyncio.sleep(0.1)

            def bSound():
                os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/b-sounds-small.mp3")
                return

            bSoundThread = Thread(target = bSound)
            bSoundThread.start()

            while danceReps < 2:
                await rvr.raw_motors(1, 90, 1, 90)
                await asyncio.sleep(1)
                await rvr.raw_motors(1, 150, 2, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)  
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)  
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 90, 2, 90)
                await asyncio.sleep(1)
                await rvr.raw_motors(1, 150, 2, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)  
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)  
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                danceReps += 1
            danceReps = 0
            danceFlag = ""

        if danceFlag == "Y":

            def ySound():
                os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/y-twerk-small.mp3")
                return

            ySoundThread = Thread(target = ySound)

            #await rvr.drive_with_heading(speed=0,heading=50,flags=0)
            #await asyncio.sleep(0.1)
            if heading >= 180:
                heading = heading - 180
            elif heading < 180:
                heading = heading + 180
            await rvr.drive_with_heading(0,heading,0)
            await asyncio.sleep(1)
            headingVar = heading

            while danceReps < 3:
                await rvr.raw_motors(2, 90, 2, 90)
                await asyncio.sleep(.3) 
                await rvr.raw_motors(1, 150, 2, 150)
                await asyncio.sleep(.1)  
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)            
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 150, 2, 150)  
                await asyncio.sleep(.1)
                await rvr.raw_motors(2, 150, 1, 150)
                await asyncio.sleep(.1)
                await rvr.raw_motors(1, 90, 1, 90)
                await asyncio.sleep(.1)
                danceReps += 1
            if heading >= 180:
                heading = heading - 180
            elif heading < 180:
                heading = heading + 180
            #print(str(heading)) 


            await rvr.drive_with_heading(0,heading,0)
            await asyncio.sleep(1)

            ySoundThread.start() 

            await asyncio.sleep(7)

            headingVar = heading 
            danceReps = 0
            danceFlag = ""

        if danceFlag == "X":

            def xSound():      
                os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/x-rodeo-small.mp3")
                return

            xSoundThread = Thread(target = xSound)
            xSoundThread.start()  

            while danceReps < 4:
                await rvr.raw_motors(1, 160, 1, 160)
                await asyncio.sleep(.2)
                await rvr.raw_motors(2, 160, 2, 160)
                await asyncio.sleep(.2)
                danceReps += 1
            danceReps = 0
            danceFlag = ""

        if danceFlag == "SELECT":
            #print(str(heading))
            if heading >= 180:
                heading = heading - 180
            elif heading < 180:
                heading = heading + 180
            #print(str(heading))
            await rvr.drive_with_heading(0,heading,0)
            await asyncio.sleep(1)
            headingVar = heading
            danceFlag = ""

        if danceFlag == "L":

            def lSound():      
                os.system("omxplayer " + "/home/pi/sphero-sdk-raspberrypi-python/projects/keyboard_control/l-trigger-small.mp3")
                return

            lSoundThread = Thread(target = lSound)
            lSoundThread.start()                  

            await asyncio.sleep(7)
            danceFlag = "" 

def run_loop():
    global loop
    global key_helper
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
        #key_helper.end_get_key_continuous()
    except IOError as err:
        print ("I/O error")
    except ValueError:
        print ("Could not convert data to an integer.")
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        breakFlag = True
        traceback.print_exc()
        print("Press any key to exit.")
        exit(1)
