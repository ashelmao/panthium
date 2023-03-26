import win32api
from win32gui import GetWindowText, GetForegroundWindow
import time

sensitivity = 2


def mouse_down():
    lmb_state = win32api.GetAsyncKeyState(0x01)
    return lmb_state < 0

moves_faster = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
moves_slower = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]

for i in range(0, sensitivity):
    moves_faster[i] = False

for i in range(0, sensitivity * 6):
    moves_slower[i] = False

print(moves_faster)

while True:
    time.sleep(0.001)
    if mouse_down():
        if GetWindowText(GetForegroundWindow()) == "Overwatch":
            if slower < 50:
                for i in range(0, 16):
                    if moves_slower[i] == True:
                        win32api.mouse_event(0x0001, 0, 1)
                    else:
                        win32api.mouse_event(0x0001, 0, 0)
                slower += 1
                print("slower")
            if slower == 50:
                for i in range(0, 16):
                    if moves_faster[i] == True:
                        win32api.mouse_event(0x0001, 0, 1)
                    else:
                        win32api.mouse_event(0x0001, 0, 0)
                print("faster")
    if not mouse_down():
        slower = 0
        time.sleep(0.001)
            