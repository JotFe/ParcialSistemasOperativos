from pynput.keyboard import Key, Listener
import time, datetime
import threading
keys=[]
cant_press=[]
instant_ini=[]
instant_end=[]
info_keys=[keys, cant_press, instant_ini, instant_end]

def on_press(key):
    TIME = time.time()
    if key not in info_keys[0]:
        info_keys[0].append(key)
        info_keys[1].append(1)
        info_keys[2].append(TIME)
        info_keys[3].append(TIME)
    else:
        for i in info_keys[0]:
            if i == key:
                position=info_keys[0].index(key)
                info_keys[1][position]=info_keys[1][position]+1
                info_keys[3][position]=TIME
    print(TIME, key, info_keys)

def on_realese(key):
    if key == Key.esc:
        return False

def report():
    timer=threading.Timer(30, report)
    timer.start()

with Listener(on_press=on_press, on_release=on_realese) as listener:
    listener.join()
