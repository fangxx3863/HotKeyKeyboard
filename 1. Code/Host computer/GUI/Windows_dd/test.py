import ctypes
from ctypes import *
import time

dd_dll = windll.LoadLibrary('DDHID64.dll')
print("调用！")

st = dd_dll.DD_btn(0) #DD Initialize
if st==1:
    print("OK")
else:
    print("Error")
    exit(101)



def PressKeys(Key):
    for i in Key:
        dd_dll.DD_key(dd_dll.DD_todc(conv_ord(i)), 1)
        print(dd_dll.DD_todc(conv_ord(i)))
    for i in reversed(Key):
        dd_dll.DD_key(dd_dll.DD_todc(conv_ord(i)), 2)

def conv_ord(ch):     # 转换类型, return: vitual_key_code
        # ch = 'q'
        if isinstance(ch, int):
            return ch
        if isinstance(ch, str):
            other_keys = {'tab': 9,
                          'clear': 12,
                          'enter': 13,
                          'shift': 16,
                          'ctrl': 17,
                          'alt': 18,
                          'pause': 19,
                          'caps_lock': 20,
                          'esc': 27,
                          'spacebar': 32,
                          'page_up': 33,
                          'page_down': 34,
                          'end': 35,
                          'home': 36,
                          'left_arrow': 37,
                          'up_arrow': 38,
                          'right_arrow': 39,
                          'down_arrow': 40,
                          'select': 41,
                          'print': 42,
                          'execute': 43,
                          'print_screen': 44,
                          'insert': 45,
                          'delete': 46,
                          'help': 47,
                          'f1': 112,
                          'f2': 113,
                          'f3': 114,
                          'f4': 116,
                          'f5': 117
            }
            for i in other_keys.keys():
                if i == ch:
                    return other_keys[i]
            if ch.islower():
                ch = ch.upper()
            return ord(ch)

PressKeys(['a', 'b'])