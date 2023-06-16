import hid
from pynput.keyboard import Controller, Key

# Hollow Knight
hollow_knight = {
    "LeftTrigger" : "k",
    "RightTrigger" : "j",
    "PadLeft" : "a", 
    "PadRight" : "d",
    "PadUp" : "w",
    "PadDown" : "s",
    "Start" : "e",
    "Select" :  Key.tab,
    "A" : " ",
    "B" : "g",
    "X" : "f",
    "Y" : "r"
}

# Celeste
celeste = {
    "LeftTrigger" : "j",
    "RightTrigger" : "f",
    "PadLeft" : "a", 
    "PadRight" : "d",
    "PadUp" : "w",
    "PadDown" : "s",
    "Start" : " ",
    "Select" :  Key.esc,
    "A" : " ",
    "B" : "x",
    "X" : "r",
    "Y" : "x"
}

keymapping = celeste

pressed_state = {character:False for character in keymapping.values()}

gamepad = hid.Device(2079, 58369)
gamepad.nonblocking = True

keyboard = Controller()

prevreport = []

def process_hid_report(report):
    buttons_down = []
    buttons_up = []

    # Left Trigger
    (buttons_down if int(bin(report[6])[-1]) else buttons_up).append("LeftTrigger")
    # Right Trigger
    (buttons_down if int(bin(report[6] + 8)[-2]) else buttons_up).append("RightTrigger")
    # Pad Left
    (buttons_down if report[0] == 0 else buttons_up).append("PadLeft")
    # Pad Right
    (buttons_down if report[0] == 255 else buttons_up).append("PadRight")
    # Pad Up
    (buttons_down if report[1] == 0 else buttons_up).append("PadUp")
    # Pad Down
    (buttons_down if report[1] == 255 else buttons_up).append("PadDown")
    # Start
    (buttons_down if int(bin(report[6] + 64)[-6]) else buttons_up).append("Start")
    # Select
    (buttons_down if int(bin(report[6] + 32)[-5]) else buttons_up).append("Select")
    
    numbinary = bin(report[5] + 256)
    # A
    (buttons_down if int(numbinary[-6]) else buttons_up).append("A")
    # B
    (buttons_down if int(numbinary[-7]) else buttons_up).append("B")    
    # X
    (buttons_down if int(numbinary[-5]) else buttons_up).append("X")
    # Y
    (buttons_down if int(numbinary[-8]) else buttons_up).append("Y")
    
    keys_to_press = [keymapping[a] for a in buttons_down]
    keys_to_unpress = [keymapping[a] for a in buttons_up if keymapping[a] not in keys_to_press]

    # Print Controller Summary
    #for element in report:
    #    print(bin(element), end=" ")
    #print("\n")
    #print("Buttons Down: " + ",".join(buttons_down))
    #print("Buttons Up: " + ",".join(buttons_up))
    #print("-----------------")

    for a in keys_to_press:
        if not pressed_state[a]:
            pressed_state[a] = True
            keyboard.press(a)
        
    for a in keys_to_unpress:
        if pressed_state[a]:
            pressed_state[a] = False
            keyboard.release(a)

while True:
    report = gamepad.read(64)
    if report and report != prevreport:
        prevreport = report
        process_hid_report(report)