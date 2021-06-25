import os
from multiprocessing import Process

def playy():
    os.system("omxplayer " + "lonely-small.mp3")


P = Process(name="playsound",target=playy)
P.start() # Inititialize Process
