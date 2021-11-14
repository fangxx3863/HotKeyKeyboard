import sys
import glob
from VirtualKey.ctypes_key import PressKey, ReleaseKey
import serial

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import pymouse
import pykeyboard

import PySimpleGUI as sg
from configobj import ConfigObj
import configobj

import multiprocessing
from multiprocessing import Process, Value, Array
from queue import Queue
import queue

import time
import ctypes

from bdtime import tt, vk       # 新版由 bd_time 改为 bdtime
from VirtualKey import keybd_event, scancode_down_up, scancodes, down_up
import bdtime
import VirtualKey


m = PyMouse()
k = PyKeyboard()
q = Queue()

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

def PressKeys(Key):
    for i in Key:
        PressKey(conv_ord(i))
    for i in reversed(Key):
        ReleaseKey(conv_ord(i))


def newConf(Name):
    config = ConfigObj("setting.ini",encoding='UTF8')
    config[Name] = {}
    config[Name]['K01'] = 'A'
    config[Name]['K02'] = 'B'
    config[Name]['K03'] = 'C'
    config[Name]['K04'] = 'D'
    config[Name]['K05'] = 'E'
    config[Name]['K06'] = 'F'
    config[Name]['K07'] = 'G'
    config[Name]['K08'] = 'H'
    config[Name]['K09'] = 'I'
    config[Name]['K10'] = 'J'
    config[Name]['K11'] = 'K'
    config[Name]['K12'] = 'L'
    config[Name]['EC1_Left'] = 'Z'
    config[Name]['EC1_SW'] = 'X'
    config[Name]['EC1_Right'] = 'C'
    config[Name]['EC2_Left'] = 'V'
    config[Name]['EC2_SW'] = 'B'
    config[Name]['EC2_Right'] = 'N'
    config.write()

def writeConf(Key, Cmd, List):
    if isinstance(Key, list):
        config = ConfigObj("setting.ini",encoding='UTF8')
        for i in Key:
            for j in Cmd:
                config[List][i] = j
                config.write()
    if isinstance(Key, str):
        config = ConfigObj("setting.ini",encoding='UTF8')
        config[List][Key] = Cmd
        config.write()

def readConf(List, Key=None):
    if Key is None:
        config = ConfigObj("setting.ini",encoding='UTF8')
        Cmd = config[List]
    else:
        config = ConfigObj("setting.ini",encoding='UTF8')
        Cmd = config[List][Key]
    return Cmd      # 返回值为CMD的Str或者CMD的字典


def readList():     # 获取全部配置名称
    config = ConfigObj("setting.ini",encoding='UTF8')
    List = config.keys()
    return List     # 返回值为一个列表包含全部配置名称

def delList(List):
    config = ConfigObj("setting.ini",encoding='UTF8')
    del config[List]
    config.write()

def decodeList(Cmd):        # 解码多按键
    if "+" in Cmd:
        decodeCmd = Cmd.split('+')
    else:
        decodeCmd = Cmd
    return decodeCmd        # 返回值要么为str要么为list

def checkList(Cmd):     # 判断配置的按键是否为多按键
    if "+" in Cmd:
        return True     # 多按键返回真
    else:
        return False        # 单按键返回假

def choiceValue(callback, t):
    decodeValue = callback[t]
    return decodeValue

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

def readLowPc(ser):
    count = ser.inWaiting() # 获取串口缓冲区数据
    recv = str(ser.readline()[0:-2].decode("utf8")) # 读出串口数据，数据采用utf8编码
    return recv     # 返回值为str

def readLowPcList(ser):
    count = ser.inWaiting() # 获取串口缓冲区数据
    recv = str(ser.readline()[0:-2].decode("utf8")) # 读出串口数据，数据采用utf8编码
    return recv.split('_')     # 返回值为list

def splitLowPcKey(key):
    return key.split('_')     # 返回值为list

def findDevice():
    tty = serial_ports()
    for devId in tty:
        ser = serial.Serial(devId, 115200)
        t = 0
        while t < 12000:
            ser.write('Check'.encode("utf8"))       # 发送Check命令
            count = ser.inWaiting() # 获取串口缓冲区数据
            t += 1
            if count !=0 :
                recv = str(ser.readline()[0:-2].decode("utf8")) # 读出串口数据，数据采用utf8编码
                if recv == "this":      # 检测下位机是否返回数据
                    return devId
                    break

def setKey(setKeyValue, newConfValue):
    device = findDevice()       # 查找下位机设备ID
    ser = serial.Serial(device, 115200)     # 初始化下位机读取
    
    PdevKeys = {'A_P': 'K01', 'B_P': 'K02', 'C_P': 'K03', 'D_P': 'K04',
                'E_P': 'K05', 'F_P': 'K06', 'G_P': 'K07', 'H_P': 'K08',
                'I_P': 'K09', 'J_P': 'K10', 'K_P': 'K11', 'L_P': 'K12',
                'SW1_P': 'EC1_SW', 'SW2_P': 'EC2_SW',
                'D1_1': 'EC1_Left', 'D1_-1': 'EC1_Right', 
                'D2_1': 'EC2_Left', 'D2_-1': 'EC2_Right'}       # 下位机按键按下的回报值字典

    RdevKeys = {'A_R': 'K01', 'B_R': 'K02', 'C_R': 'K03', 'D_R': 'K04',
                'E_R': 'K05', 'F_R': 'K06', 'G_R': 'K07', 'H_R': 'K08',
                'I_R': 'K09', 'J_R': 'K10', 'K_R': 'K11', 'L_R': 'K12',
                'SW1_R': 'EC1_SW', 'SW2_R': 'EC2_SW'}       # 下位机按键松开的回报值字典
    
    allList = readList()        # 读取配置文件中的全部配置
    nowConf = readConf(allList[setKeyValue.value])      # CMD的字典
    while True:
        if newConfValue.value == 1:     # 当按下新建配置后重新读取配置文件中的全部配置
            allList = readList()
            nowConf = readConf(allList[setKeyValue.value])      # CMD的字典
            newConfValue.value = 0
        key = readLowPc(ser)        # 读取下位机回报数据

        # Press
        for i in PdevKeys.keys():
            if newConfValue.value == 1:     # 当按下新建配置后重新读取配置文件中的全部配置
                allList = readList()
                nowConf = readConf(allList[setKeyValue.value])      # CMD的字典
                newConfValue.value = 0
            if key == i:
                if checkList(nowConf[PdevKeys[i]]) is True:     # 有加号
                    PressKeys(decodeList(nowConf[PdevKeys[i]]))      # 有问题，暂时用回旧方案（已修复）
                    # k.press_keys(decodeList(nowConf[PdevKeys[i]]))
                elif checkList(nowConf[PdevKeys[i]]) is False:      # 没有加号
                    if nowConf[PdevKeys[i]] == 'left':
                        m.scroll(1, 0)
                    elif nowConf[PdevKeys[i]] == 'right':
                        m.scroll(-1, 0)
                    elif nowConf[PdevKeys[i]] == 'up':
                        m.scroll(0, 1)
                    elif nowConf[PdevKeys[i]] == 'down':
                        m.scroll(0, -1)
                    else:
                        PressKey(conv_ord(nowConf[PdevKeys[i]]))

        # Release
        for i in RdevKeys.keys():
            if newConfValue.value == 1:     # 当按下新建配置后重新读取配置文件中的全部配置
                allList = readList()
                nowConf = readConf(allList[setKeyValue.value])      # CMD的字典
                newConfValue.value = 0
            if key == i:
                if checkList(nowConf[RdevKeys[i]]) is False:        # 没有加号
                    for k in decodeList(nowConf[RdevKeys[i]]):
                        ReleaseKey(conv_ord(k.upper()))
        
    

        
# 窗口持久化
def gui():
    # 设置pysimplegui主题，不设置的话就用默认主题
    sg.ChangeLookAndFeel('DarkAmber')
    # 定义2个常量，供下面的layout直接调用，就不用一个个元素来调字体了
    # 字体和字体大小
    FONT1 = (16)
    FONT2 = (20)
    FONT3 = (30)
    # 让下拉菜单内容填充为全部配置名称
    Comobo = readList()
    # 界面布局
    layout = [
        [sg.Text('EC1配置', font=(FONT2), size=(20, 1))],
        [sg.Text('左转'), sg.InputText('<--', key='EC1_Left', size=(10, 5), font=(FONT1)), sg.Text('中键'), sg.InputText('SW', key='EC1_SW', size=(10, 5), font=(FONT1)), sg.Text('右转'), sg.InputText('-->', key='EC1_Right', size=(10, 5), font=(FONT1)), ],
        [sg.Text('EC2配置', font=(FONT2), size=(20 ,1))],
        [sg.Text('左转'), sg.InputText('<--', key='EC2_Left', size=(10, 5), font=(FONT1)), sg.Text('中键'), sg.InputText('SW', key='EC2_SW', size=(10, 5), font=(FONT1)), sg.Text('右转'), sg.InputText('-->', key='EC2_Right', size=(10, 5), font=(FONT1)), ],
        [sg.HorizontalSeparator()],

        [sg.Text('自定义按键配置', font=(FONT2))],
        [sg.Text('K01'), sg.InputText('K01', key='K01', size=(10, 8), font=(FONT3)), sg.Text('K02'), sg.InputText('K02', key='K02', size=(10, 8), font=(FONT3)), sg.Text('K03'), sg.InputText('K03', key='K03', size=(10, 8), font=(FONT3)), sg.Text('K04'), sg.InputText('K04', key='K04', size=(10, 8), font=(FONT3)), ],
        [sg.Text('K05'), sg.InputText('K05', key='K05', size=(10, 8), font=(FONT3)), sg.Text('K06'), sg.InputText('K06', key='K06', size=(10, 8), font=(FONT3)), sg.Text('K07'), sg.InputText('K07', key='K07', size=(10, 8), font=(FONT3)), sg.Text('K08'), sg.InputText('K08', key='K08', size=(10, 8), font=(FONT3)), ],
        [sg.Text('K09'), sg.InputText('K09', key='K09', size=(10, 8), font=(FONT3)), sg.Text('K10'), sg.InputText('K10', key='K10', size=(10, 8), font=(FONT3)), sg.Text('K11'), sg.InputText('K11', key='K11', size=(10, 8), font=(FONT3)), sg.Text('K12'), sg.InputText('K12', key='K12', size=(10, 8), font=(FONT3)), ],
        [sg.HorizontalSeparator()],

        [sg.Combo(Comobo, size=(8, 1), font=(FONT2), key='_nowList', default_value="DEFAULT"), sg.Btn('新建配置', key='_newConf', font=(FONT2), size=(8, 1)), sg.Btn('删除配置', key='_delConf', font=(FONT2), size=(8, 1)), sg.Btn('读取配置', key='_readConf', font=(FONT2), size=(8, 1)), sg.Btn('保存配置', key='_saveConf', font=(FONT2), size=(8, 1)), sg.Btn('配置说明', key='_aboutConf', font=(FONT2), size=(8, 1)), sg.Btn('关于', key='_about', font=(FONT2), size=(8, 1))]

    ]
    # 创建窗口，引入布局，并进行初始化
    # 创建时，必须要有一个名称，这个名称会显示在窗口上
    window = sg.Window('HotKeyKeyboard驱动程序', layout=layout, finalize=True)
    # 创建一个事件循环，否则窗口运行一次就会被关闭
    while True:
        # 监控窗口情况
        event, value = window.Read()
        # 当获取到事件时，处理逻辑（按钮绑定事件，点击按钮即触发事件）
        # sg.Input(),sg.Btn()都带有一个key，监控它们的状况，读取或写入信息

        if event == '_newConf':
            newConfName = sg.PopupGetText('配置名称')       # 弹窗获取新建配置文件的名称
            newConf(newConfName)        # 向配置文件中添加新配置
            Comobo = readList()     # 获取现在配置文件中的全部配置（列表）
            window.Element("_nowList").Update(value=newConfName, values=Comobo)     # 更新下拉菜单
            

        if event == '_readConf':
            nowList = value['_nowList']     # 读GUI里的选配置下拉菜单的值
            
            Cmd = readConf(nowList)     # 读取现在的配置文件（字典）
            keys = Cmd.keys()   # 获取现在的配置文件的字典的全部键值（列表）

            setKeyValue.value = readList().index(nowList)   # 传递现在的配置文件名称至共享变量
            newConfValue.value = 1      # 向共享变量传递参数

            i = 0
            for i in keys:      # 遍历现在的配置文件的字典的全部键值
                sgCmd = Cmd[i]      # 获取现在的配置的字典的第i个值
                print("keys: " + i + " sgCmd: " + sgCmd)
                window[i].Update(value=sgCmd)       # 更新现在的配置的字典的第i个值的文本输入框内容为sgCmd

        if event == '_saveConf':
            uiKeys = ['K01', 'K02', 'K03', 'K04', 
                      'K05', 'K06', 'K07', 'K08',
                      'K09', 'K10', 'K11', 'K12', 
                      'EC1_Left', 'EC1_SW', 'EC1_Right', 
                      'EC2_Left', 'EC2_SW', 'EC2_Right']        # GUI内全部自定义按键的ID
            newConfValue.value = 1      # 向共享变量传递参数
            i = 0
            for i in uiKeys:
                writeConf(i, value[i], value['_nowList'])       # 更新选定配置文件的值到GUI
        
        if event == '_delConf':
            nowList = value['_nowList']     # 读GUI里的选配置下拉菜单的值
            delList(nowList)
            Comobo = readList()     # 获取现在配置文件中的全部配置（列表）
            window.Element("_nowList").Update(value='DEFAULT', values=Comobo)     # 更新下拉菜单
        
        if event == '_aboutConf':
            sg.PopupAnnoying('配置说明\n1. 按下单个按键请输入单个按键名称\n2. 按下多个按键请以“+”为分隔符输入多个按键名称\n3. 鼠标滚轮对应键为，上：up，下：down，左：left，右：right\n4. 多功能键请输入全称，如Command，Alt，Ctrl', font=(FONT2))

        if event == '_about':
            sg.PopupAnnoying('作者碎碎念\n\n这算是我用Py写的第一个图形化软件，不得不说图形化真的很难写\n要去想要去设计要去注意的点太多了。\n在写这个程序的时候我经常写到一半就忘记了之前写过什么功能\n导致这个软件花了我一个晚上才糊出来(笑)。\n希望能够正常运行吧！\n', font=(FONT2))

        if event is None:
            tKey.terminate()
            break
    window.close()
   


if __name__ == '__main__':
    # 初始化多进程
    multiprocessing.freeze_support()

    # 初始化共享变量
    setKeyValue = Value("i", 0)
    newConfValue = Value("i", 0)
    tKey = Process(target=setKey, daemon=True, args=(setKeyValue, newConfValue, ))

    # 启动映射及GUI
    tKey.start()
    gui()
    