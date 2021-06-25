import signal
import keyboard
import time

class MyKeyEventClass1(object):
  def __init__(self):
    self.done = False
    signal.signal(signal.SIGINT, self.cleanup)
    keyboard.hook(self.my_on_key_event)
    while not self.done:
      time.sleep(1)  #  Wait for Ctrl+C

  def cleanup(self, signum, frame):
    self.done = True

  def my_on_key_event(self, e):
   # if str(e) == 'KeyboardEvent(w up)':
   print("Got key release event: " + str(e))

a = MyKeyEventClass1()
