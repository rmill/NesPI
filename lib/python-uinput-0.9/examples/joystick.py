import uinput

def main():
    events = (
        uinput.BTN_JOYSTICK,
        uinput.ABS_X + (0, 255, 0, 0),
        uinput.ABS_Y + (0, 255, 0, 0),
        )

    device = uinput.Device(events)

    for i in range(20):
        # syn=False to emit an "atomic" (5, 5) event.
        device.emit(uinput.ABS_X, 5, syn=False)
        device.emit(uinput.ABS_Y, 5)

    device.emit(uinput.BTN_JOYSTICK, 1) # Press.
    device.emit(uinput.BTN_JOYSTICK, 0) # Release.

if __name__ == "__main__":
    main()
