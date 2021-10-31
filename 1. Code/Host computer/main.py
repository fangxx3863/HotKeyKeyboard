import sys
import glob
import serial
from pymouse import PyMouse
from pykeyboard import PyKeyboard

m = PyMouse()
k = PyKeyboard()

modelSwitch = "Multiple"    #键盘区Multiple(多个按键)或者Single(单个按键)
ECmodelSwitch = "Scroll"    #旋钮区Multiple(多个按键)或者Scroll(鼠标滚轮)
SWmodelSwitch = "Single"    #旋钮按键区Multiple(多个按键)或者Scroll(鼠标滚轮)

# 旋转编码器
EC1p = ['']
EC1r = ['']

EC2p = ['']
EC2r = ['']

# 单键列表
keyA = "A"
keyB = "B"
keyC = "C"
keyD = "D"

keyE = "E"
keyF = "F"
keyG = "G"
keyH = "H"

keyI = "I"
keyJ = "J"
keyK = "K"
keyL = "L"

SW1 = "Command"
SW2 = "Shift"

# 组合键列表
MkeyA = ['A', ]
MkeyB = ['Space']
MkeyC = ['Command', "-"]
MkeyD = ['Command', "="]

MkeyE = ['E', ]
MkeyF = ['F', ]
MkeyG = ['G', ]
MkeyH = ['H', ]

MkeyI = ['I', ]
MkeyJ = ['J', ]
MkeyK = ['K', ]
MkeyL = ['L', ]

MSW1 = ['Shift', ]
MSW2 = ['Command', ]

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal"/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def showTtyDev():
    tty = serial_ports()
    id = 0
    for i in tty:
        print(str(id) + ". " + str(i))
        id = id + 1

def singlePress():
    if recv == "A_P":
        k.press_key(keyA)
        print("Key A Press")
    elif recv == "A_R":
        k.release_key(keyA)
        print("Key A Release")

    if recv == "B_P":
        k.press_key(keyB)
        print("Key B Press")
    elif recv == "B_R":
        k.release_key(keyB)
        print("Key B Release")

    if recv == "C_P":
        k.press_key(keyC)
        print("Key C Press")
    elif recv == "C_R":
        k.release_key(keyC)
        print("Key C Release")

    if recv == "D_P":
        k.press_key(keyD)
        print("Key D Press")
    elif recv == "D_R":
        k.release_key(keyD)
        print("Key D Release")

    if recv == "E_P":
        k.press_key(keyE)
        print("Key E Press")
    elif recv == "E_R":
        k.release_key(keyE)
        print("Key E Release")

    if recv == "F_P":
        k.press_key(keyF)
        print("Key F Press")
    elif recv == "F_R":
        k.release_key(keyF)
        print("Key F Release")

    if recv == "G_P":
        k.press_key(keyG)
        print("Key G Press")
    elif recv == "G_R":
        k.release_key(keyG)
        print("Key G Release")

    if recv == "H_P":
        k.press_key(keyH)
        print("Key H Press")
    elif recv == "H_R":
        k.release_key(keyH)
        print("Key H Release")

    if recv == "I_P":
        k.press_key(keyI)
        print("Key I Press")
    elif recv == "I_R":
        k.release_key(keyI)
        print("Key I Release")

    if recv == "J_P":
        k.press_key(keyJ)
        print("Key J Press")
    elif recv == "J_R":
        k.release_key(keyJ)
        print("Key J Release")

    if recv == "K_P":
        k.press_key(keyK)
        print("Key K Press")
    elif recv == "K_R":
        k.release_key(keyK)
        print("Key K Release")

    if recv == "L_P":
        k.press_key(keyL)
        print("Key L Press")
    elif recv == "L_R":
        k.release_key(keyL)
        print("Key L Release")

def multiplePress():
    if recv == "A_P":
        k.press_keys(MkeyA)
        print("Key A Press")

    if recv == "B_P":
        k.press_keys(MkeyB)
        print("Key B Press")

    if recv == "C_P":
        k.press_keys(MkeyC)
        print("Key C Press")

    if recv == "D_P":
        k.press_keys(MkeyD)
        print("Key D Press")

    if recv == "E_P":
        k.press_keys(MkeyE)
        print("Key E Press")

    if recv == "F_P":
        k.press_keys(MkeyF)
        print("Key F Press")

    if recv == "G_P":
        k.press_keys(MkeyG)
        print("Key G Press")

    if recv == "H_P":
        k.press_keys(MkeyH)
        print("Key H Press")

    if recv == "I_P":
        k.press_keys(MkeyI)
        print("Key I Press")

    if recv == "J_P":
        k.press_keys(MkeyJ)
        print("Key J Press")

    if recv == "K_P":
        k.press_keys(MkeyK)
        print("Key K Press")

    if recv == "L_P":
        k.press_keys(MkeyL)
        print("Key L Press")

def multipleSW():
    if recv == "SW1_P":
        k.press_keys(MSW1)
        print("Key SW1 Press")

    if recv == "SW2_P":
        k.press_keys(MSW2)
        print("Key SW2 Press")

def singleSW():
    if recv == "SW1_P":
        k.press_key(SW1)
        print("Key SW1 Press")
    elif recv == "SW1_R":
        k.release_key(SW1)
        print("Key SW1 Release")

    if recv == "SW2_P":
        k.press_key(SW2)
        print("Key SW2 Press")
    elif recv == "SW2_R":
        k.release_key(SW2)
        print("Key SW2 Release")

def ECMultiple():
    if recv == "D1_1_P":
        k.press_keys(EC1p)
        print("Key EC1+ Press")
    elif recv == "D1_-1_P":
        k.press_keys(EC1r)
        print("Key EC1- Press")
    if recv == "D2_1_P":
        k.press_keys(EC2p)
        print("Key EC2+ Press")
    elif recv == "D2_-1_P":
        k.press_keys(EC2r)
        print("Key EC2- Press")

def ECScroll():
    if recv == "D1_1_P":
        m.scroll(-1, 0)
        print("Key EC1+ Press")
    elif recv == "D1_-1_P":
        m.scroll(1, 0)
        print("Key EC1- Press")
    if recv == "D2_1_P":
        m.scroll(0, -1)
        print("Key EC2+ Press")
    elif recv == "D2_-1_P":
        m.scroll(0, 1)
        print("Key EC2- Press")

if __name__ == '__main__':
    showTtyDev()
    devId = input("Choice your tty id: ")
    dev = serial_ports()
    print(str(dev[int(devId)]))
    ser = serial.Serial(dev[int(devId)], 115200)
    while True:
        count = ser.inWaiting() # 获取串口缓冲区数据
        if count !=0 :
            recv = str(ser.readline()[0:-2].decode("utf8")) # 读出串口数据，数据采用utf8编码
            #print(str(ser.readline()[0:-2].decode("utf8"))) # 打印一下子
            if modelSwitch == "Multiple":
                multiplePress()
            elif modelSwitch == "Single":
                singlePress()
            
            if ECmodelSwitch == "Multiple":
                ECMultiple()
            elif ECmodelSwitch == "Scroll":
                ECScroll()

            if SWmodelSwitch == "Multiple":
                multipleSW()
            elif SWmodelSwitch ==  "Single":
                singleSW()
            