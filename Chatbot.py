# pylint: disable=bad-option-value,line-too-long, too-many-lines, global-statement, invalid-name, bare-except,super-init-not-called, missing-module-docstring, unused-import, unused-argument, consider-iterating-dictionary, consider-using-f-string, eval-used

import sys
import threading
import time
from random import choice
from re import search

import TAPI
import Variables
from irc.bot import SingleServerIRCBot
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from requests import get

authtok = ""
refreshtok = ""
COOLDOWN = False
CURRENT_CD_TIMER = 0

class Bot(SingleServerIRCBot):
    """ IRC chat bot class for handling Twitch IRC chat messages/commands."""

    def __init__(self):
        """ Initialization function for irc bot class. """

        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = "<insert username here>".lower()
        self.CLIENT_ID = "<insert client id here>"
        self.TOKEN = "<insert client secret here>"
        self.CHANNEL = ""
        self.channel_id = ""

    def connect_to_chat(self):
        """Function to connect chat bot to irc channel"""

        self.CHANNEL = "#"+str(Variables.STREAMER['streamer']).lower()
        url = f"https://api.twitch.tv/helix/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID,
                   "Authorization": "Bearer " + Variables.TOKENS['auth']}
        resp = get(url, headers=headers, timeout=10).json()
        self.channel_id = resp["data"][0]["id"]

        super().__init__(
            [(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        """Function that triggers on irc channel connection. """

        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        Variables.CHATBOXSETTINGS['msgid'] = 0
        Variables.CHATBOXSETTINGS['msgchecklst'] = {}
        Variables.CHATBOXSETTINGS['msgcolors'] = {}
        Variables.CHATBOXSETTINGS['msgdict'] = []
        Variables.CHATBOXSETTINGS['datalist'] = []
        if Variables.CHATBOXSETTINGS['disabledusers'] == '':
            Variables.CHATBOXSETTINGS['disabledusers'] = []
        else:
            try:
                Variables.CHATBOXSETTINGS['disabledusers'] = eval(Variables.CHATBOXSETTINGS['disabledusers'])
            except:
                Variables.CHATBOXSETTINGS['disabledusers'] = Variables.CHATBOXSETTINGS['disabledusers']

    def on_clearmsg(self, cxn, event):
        """function to clear a specific message from the chat websource."""
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        remid = tags['target-msg-id']
        keystorem = []
        for k,v in Variables.CHATBOXSETTINGS['msgchecklst'].items():
            if k == remid:
                Variables.CHATBOXSETTINGS['datalist'].append(v)
                keystorem.append(k)
        for i in keystorem:
            del Variables.CHATBOXSETTINGS['msgchecklst'][i]
        Variables.CHATBOXSETTINGS['remupdate'] = True

    def on_clearchat(self, cxn, event):
        """ Function to clear chat websource."""
        Variables.CHATBOXSETTINGS['refresh'] = True

    def on_action(self, cxn, event):
        """ Function to handle Twitch IRC commands. """
        action = '1'
        bot.message_calc(cxn, event, action)

    def on_pubmsg(self, cxn, event):
        """ Function to handle Twitch IRC chat messages."""
        action = '0'
        bot.message_calc(cxn, event, action)

    def send_message(self, message):
        """ Function to send messages on the twitch chat."""
        self.connection.privmsg(self.CHANNEL, message)

    def mod_check(self, user):
        """Function to check if user is a mod or streamer, returns True if valid."""
        if user["ismod"] == "1":
            return True
        if str(user["name"]).lower() == str(Variables.STREAMER['streamer']).lower():
            return True

    def message_calc(self, cxn, event, action):
        """ Function to handle Twitch IRC chat messages."""
        colorlst = ['rgb(255, 0, 0)', 'rgb(0, 0, 255)', 'rgb(0, 128, 0)', 'rgb(178, 34, 34)', 'rgb(255, 127, 80)', 'rgb(154,205, 50)', 'rgb(255, 69, 0)', 
        'rgb(46, 139, 87)', 'rgb(218, 165, 32)', 'rgb(210, 105, 30)', 'rgb(95, 158, 160)', 'rgb(30, 144, 255)', 'rgb(255, 105, 180)', 'rgb(138, 43, 226)', 'rgb(0, 255, 127)']
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"], "emote": tags["emotes"], "badges": tags["badges"], "color": tags["color"], "ismod": tags["mod"], "twmsgid": tags["id"]}
        message = event.arguments[0]
        usercol = user['color']
        if user['color'] is None:
            if user['name'] not in Variables.CHATBOXSETTINGS['msgcolors'].keys():
                Variables.CHATBOXSETTINGS['msgcolors']['{}'.format(user['name'])] = choice(colorlst)
                usercol = Variables.CHATBOXSETTINGS['msgcolors']['{}'.format(user['name'])]
            else:
                usercol = Variables.CHATBOXSETTINGS['msgcolors']['{}'.format(user['name'])]
        Variables.CHATBOXSETTINGS['msgid'] += 1
        Variables.CHATBOXSETTINGS['msgchecklst']['{}'.format(user["twmsgid"])] = "{},{},{}".format(user["name"], message, Variables.CHATBOXSETTINGS['msgid'])
        Variables.CHATBOXSETTINGS['msgdict'].append({'badges': user["badges"], 'emotes': user["emote"], 'color': usercol, 'message': message, 'username': user["name"], 'msgid': str(Variables.CHATBOXSETTINGS['msgid']), 'action': action})
        Variables.CHATBOXSETTINGS['addupdate'] = True

bot = Bot()
stop_event = threading.Event()

def startbot():
    """Function for initializing the bot"""
    global authtok
    global refreshtok
    authtok = Variables.TOKENS['auth']
    refreshtok = Variables.TOKENS['refresh']
    stop_event.clear()
    chatbotconnect = threading.Thread(target=bot.connect_to_chat, daemon=True)
    chatbotconnect.start()
    time.sleep(1)
    chatbotstart = threading.Thread(target=bot.start, daemon=True, args=(stop_event,))
    chatbotstart.start()
