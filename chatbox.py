
import os
import threading
import time
from tkinter import *
from tkinter import colorchooser, filedialog, messagebox, ttk

import BrowserSources
import Chatbot
import TAPI
import Variables

Variables.MAIN_DIRECTORY = os.getcwd()
cbtop = Tk()

def chatexiting():
    Variables.CONFIG_FLAG = True
    while Variables.CONFIG_FLAG:
        time.sleep(.01)
    cbtop.destroy()

def chatchangefnt():
    Variables.CHATBOXSETTINGS['FontName'] = chatnameoffont.get()
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "Chatbox font has been changed!")

def chatchangefntcolor():
    color_code = colorchooser.askcolor(title="Choose color", parent=cbtop)
    Variables.CHATBOXSETTINGS['FontColor'] = color_code[1]
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "Chatbox font color has been changed!")

def chatchangebgcolor():
    color_code = colorchooser.askcolor(title="Choose color", parent=cbtop)
    Variables.CHATBOXSETTINGS['bgcolor'] = color_code[1]
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "Chatbox background color has been changed!")

def setopac(val):
    opacval2 = (int(val)+1)*-1
    tplist = ['FF','FC','FA','F7','F5','F2','F0','ED','EB','E8','E6','E3','E0','DE','DB','D9','D6','D4','D1','CF','CC','C9','C7','C4','C2','BF','BD','BA','B8','B5','B3','B0',
    'AD','AB','A8','A6','A3','A1','9E','9C','99','96','94','91','8F','8C','8A','87','85','82','80','7D','7A','78','75','73','70','6E','6B','69','66','63','61','5E','5C','59',
    '57','54','52','4F','4D','4A','47','45','42','40','3D','3B','38','36','33','30','2E','2B','29','26','24','21','1F','1C','1A','17','14','12','0F','0D','0A','08','05','03',
    '00']
    opacval = tplist[opacval2]
    Variables.CHATBOXSETTINGS['opacity'] = opacval
    Variables.CHATBOXSETTINGS['sldropac'] = val

def chatfontcap():
    Variables.CHATBOXSETTINGS['FontCap'] = int(chatcapvar1.get())
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "Chatbox font has been capitalized!"
    )

def disabletccmds():
    Variables.CHATBOXSETTINGS['disabledcmds'] = int(capvarchat.get())
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "Commands disabled in chatbox!"
    )

def remdisableduser():
    usertorem = str(disuserlst.get())
    while usertorem in list(Variables.CHATBOXSETTINGS['disabledusers']):
        list(Variables.CHATBOXSETTINGS['disabledusers']).remove(usertorem)
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "{} has been disabled from the chatbox!".format(usertorem)
    )


def adddisableduser():
    list(Variables.CHATBOXSETTINGS['disabledusers']).append(disuserentry.get())
    messagebox.showinfo(
    icon="question",
    parent=cbtop,
    title = "Success!",
    message = "{} has been disabled from the chatbox!".format(str(disuserentry.get()))
    )

def refresh_emotes():
    emotefetcher = threading.Thread(target=TAPI.emotes.emotefetcher, daemon=True)
    emotefetcher.start()

maingeo = str(Variables.WINDOWLOCATION['WinGeo'])
cbtop.geometry(maingeo)
cbtop.iconbitmap("icons\\boticon.ico")
cbtop.title("Chatbox Settings")

chatlblfont = Label(
    cbtop, text="Select a Font for the chat", font=("Calibri Bold", 10), bg="grey30", fg="black"
)
chatlblfont.place(x=25, y=0)
chatnameoffont = StringVar(
    value=str(Variables.CHATBOXSETTINGS['FontName']))
chatfontdir = str(Variables.MAIN_DIRECTORY + "\\static\\fonts")
print(chatfontdir)
chatfontdrop = ttk.Combobox(cbtop, textvariable=chatnameoffont)
chatfontdrop["values"] = os.listdir(chatfontdir)
chatfontdrop["state"] = "readonly"
chatfontdrop.place(x=10, y=20)
chatfontsize = StringVar()
chatfontsize.set(Variables.CHATBOXSETTINGS['FontSize'])
chatfontsizeentry = Entry(
    cbtop, width=17, bg="grey", textvariable=chatfontsize, font=("Calibri", 12)
)
chatfontsizeentry.place(x=10, y=42)
chatfontstate = int(Variables.CHATBOXSETTINGS['FontCap'])
chatcapvar1 = IntVar(value=chatfontstate)
chatcapbox = Checkbutton(
    cbtop,
    text="Capitalize Text",
    variable=chatcapvar1,
    onvalue=1,
    offvalue=0,
    command=chatfontcap,
    font=("Calibri Bold", 10),
    bg="grey30",
    fg="black",
)
chatcapbox.place(x=10, y=95)

chatstate = int(Variables.CHATBOXSETTINGS['disabledcmds'])
capvarchat = IntVar(value=chatstate)
capboxdischats = Checkbutton(
    cbtop,
    text="Disable Commands",
    variable=capvarchat,
    onvalue=1,
    offvalue=0,
    command=disabletccmds,
    font=("Calibri Bold", 10),
    bg="grey30",
    fg="black",
)
capboxdischats.place(x=10, y=117)
chatconfirmfont = Button(cbtop, text="Confirm", command=chatchangefnt)
chatconfirmfont.place(x=50, y=70)
chatfontcolorpick = Button(cbtop, text="Pick Chat Font Color",
                            command=chatchangefntcolor)
chatfontcolorpick.place(x=25, y=140)
chatbgcolorpick = Button(cbtop, text="Pick Chat Background Color",
                            command=chatchangebgcolor)
chatbgcolorpick.place(x=25, y=170)
opacsld = Scale(
cbtop,
length=100,
bg="grey30",
label="Opacity",
orient=HORIZONTAL,
highlightbackground="grey30",
from_=0,
to=100,
resolution=1,
font=("Calibri", 10, "bold"),
command=setopac,
)
opacsld.place(x=10, y=200)
opacsld.set(Variables.CHATBOXSETTINGS['sldropac'])

chatlbldisuser = Label(
    cbtop, text="Add/Remove users from chatbox", font=("Calibri Bold", 10), bg="grey30", fg="black"
)
chatlbldisuser.place(x=210, y=0)

disuserlst = StringVar(
    value='Select User')
chatdisuserdrop = ttk.Combobox(cbtop, textvariable=disuserlst, width=19)
chatdisuserdrop["values"] = list(Variables.CHATBOXSETTINGS['disabledusers'])
chatdisuserdrop["state"] = "readonly"
chatdisuserdrop.place(x=210, y=22)
disusertxt = StringVar()
disusertxt.set('Type user name here')
disuserentry = Entry(
    cbtop, width=19, bg="grey", textvariable=disusertxt, font=("Calibri", 12)
)
disuserentry.place(x=210, y=52)
adddisuser = Button(cbtop, text="Disable User",
                            command=adddisableduser)
adddisuser.place(x=375, y=50)
refreshemotes = Button(cbtop, text="Refresh Emotes",
                            command=refresh_emotes)
refreshemotes.place(x=210, y=80)
remdisuser = Button(cbtop, text="Enable User",
                            command=remdisableduser)
remdisuser.place(x=375, y=20)

cbtop.protocol("WM_DELETE_WINDOW", chatexiting)

if __name__ == "__main__":
    twitchstart = threading.Thread(target=TAPI.startup, daemon=True)
    chatbotstart = threading.Thread(target=Chatbot.startbot, daemon=True)
    websourcesstart = threading.Thread(target=BrowserSources.start_web_sources, daemon=True)
    websourcesstart.start()
    twitchstart.start()
    time.sleep(10)
    chatbotstart.start()
    cbtop.configure(bg="grey30")
    cbtop.mainloop()
