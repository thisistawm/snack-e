import signal
import keyboard
import time
class MyKeyEventClass1(object):
  def __init__(self):
    self.__callback = None
    self.done = False
    signal.signal(signal.SIGINT, self.cleanup)
    keyboard.hook(self.my_on_key_event)
  def cleanup(self, signum, frame):
    self.done = True
  def set_callback(self, callback):
    self.__callback = callback
  def my_on_key_event(self, e):
    if (__callback != None):
      self.__callback(e)
