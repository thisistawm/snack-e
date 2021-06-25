#Edit: added so python 3 and 2 can be used
try:
	from Tkinter import *
except:
	from tkinter import *

dbnm = Tk()
def key_input(event):
	print("I saw: ", event.char)
def key_stop(event):
	print("I saw: ", event.char)

dbnm.bind('<KeyPress>', key_input)
dbnm.bind('<KeyRelease>',key_stop)
dbnm.mainloop()
