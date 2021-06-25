import inputs

print(inputs.devices.gamepads)

while True:
    events = inputs.get_gamepad()
    for event in events:
       eventCode = (str(event.code) + str(event.state))

    print(eventCode)


    if "ABS_Y0" in eventCode:
        print("up detected")

    if "ABS_Y127" in eventCode:
        print("release detected")

    if "ABS_Y255" in eventCode:
        print("down detected")
