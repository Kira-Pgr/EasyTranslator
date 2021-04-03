import requests
import json
import win32clipboard
from tkinter import messagebox
import ctypes
from tkinter import *
import os
import clipboard
import pyperclip
import time
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''' --------------------------------------翻易器(EasyTranslator) ver 1.0.0------------------------'''
'''                                                           By：Kira_Pgr                                                 ''' 
'''                                              ref:有道翻译API, StackOverFlow                                '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
url = 'https://aidemo.youdao.com/trans'
#关于窗口
def AboutBox():
    messagebox.showinfo("关于EasyTranslator", "-------------------翻易器(EasyTranslator)v1.0.0--------------------\n作者:Kira_Pgr\nref:有道翻译API, StackOverFlow\n安装包:The_Void, auto-py-to-exe, WinZip")
#通过requests调用API                                 
def translate(text, *args):
    try:
        data = {"q": text, "from": "auto", "to": args}
        resp = requests.post(url, data)
    except:
        return None
    return resp
#将结果print进文件（暴力出奇迹, 啊不 = =） 逃）
def printrst(resp):
  with open('output.txt', 'w') as f:
    if resp is not None and resp.status_code == 200:
        respJson = json.loads(resp.text)
        print(" </> 翻译结果:", file = f)
        if "translation" in respJson:
                print("       一般释义:", file = f)
                print("\n".join(' ' * 9 + '' + str(i) for i in respJson["translation"]), file=f)
        if "basic" in respJson and "explains" in respJson["basic"]:
                print( "       基本释义:", file = f)
                print("\n".join(' ' * 9 + '' + str(i) for i in respJson["basic"]["explains"]), file=f)
        if "web" in respJson:
                print("       网络释义:", file = f)
                index = 1
                for i in respJson["web"]:
                    print("         %d. %s:" % (index, i["key"]), file = f)
                    print("\n".join(' ' * 14 + '' + str(i) for i in i["value"]), file=f)
                    index += 1
    f.close()
#函数connect:连接窗口最小化事件和函数ClipBoard_Check
def connect():
    a = ''
    Etr_GUI.bind('<Unmap>', ClipBoard_Check)
    ClipBoard_Check(a)
#函数connect:取消窗口最小化事件和函数ClipBoard_Check的连接
def disconnect():
    Etr_GUI.unbind('<Unmap>', ClipBoard_Check)
#函数Easy_Translator_Core_Module: UI与其他操作的交互
def Easy_Translator_Core_Module(text):
    args = "zh-CHS"
    resp = translate(text, args)
    cwd = os.getcwd()
    printrst(resp)
    with open('output.txt', 'r') as f:
           conteudo = f.read()
    if os.path.exists("output.txt"):
       os.remove("output.txt")
       return conteudo
#函数ClipBoard_Check：检测剪贴板内容是否被修改（用户是否复制了要翻译的内容）
def ClipBoard_Check(a):
    recent_value = pyperclip.paste()
    while True:
         tmp_value = pyperclip.paste()
         if tmp_value != recent_value:
               recent_value = tmp_value
               Etr_GUI.deiconify()
               auto()
               break;
#函数auto:自动模式
def auto():
        text1.delete(0.0, END)
        text2.delete(0.0, END)
        text = pyperclip.paste()
        text1.insert(0.0, text)
        t2 = Easy_Translator_Core_Module(text)
        text2.insert(0.0, t2)
        mainloop()
#函数manual:点下翻译键        
def manual():
    text2.delete(0.0, END)
    text2.insert(0.0, Easy_Translator_Core_Module(text1.get(0.0, END)))

a = ''  #这句嘛= = 防error
#隐藏控制台
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)
#UI部分
Etr_GUI = Tk()
Etr_GUI.title("Easy Translator")
Label(Etr_GUI, text="----------翻易器v1.0.0--------").grid(row=0, sticky=W)
text1 = Text(Etr_GUI, height=30, width=50)
text1.grid(row=3, sticky=W)
text1.insert(END, "请把原文放这里哦~")
text2 = Text(Etr_GUI, height=30, width=50)
text2.grid(row=3, column = 2)
text2.insert(END, "这里是你的译文= =")
s1 = Scrollbar(Etr_GUI, command=text1.yview)
s1.grid(row=3, column=1, sticky=S + W + E + N)
s2 = Scrollbar(Etr_GUI, command=text2.yview)
s2.grid(row=3, column=10, sticky=S + W + E + N)
Button(Etr_GUI, text="翻译", command=manual).grid(row = 2, sticky=W)
Button(Etr_GUI, text="启动自动模式", command=connect).grid(row = 50, sticky=W)
Button(Etr_GUI, text="关闭自动模式", command=disconnect).grid(row = 50, column = 2)
Button(Etr_GUI, text="关于", command=AboutBox).grid(row = 50)
mainloop()
