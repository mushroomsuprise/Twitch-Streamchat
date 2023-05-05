# pylint: disable=bad-option-value,line-too-long, too-many-lines, global-statement, invalid-name, bare-except, eval-used, unused-import, missing-module-docstring, pointless-statement

import os

import requests
from engineio.async_drivers import gevent
from engineio.payload import Payload
from flask import Flask, render_template
from flask_socketio import SocketIO

import TAPI
import Variables

TEMPLATE_FOLDER = os.getcwd() + "\\templates"
STATIC_FOLDER = os.getcwd() + "\\static"
Payload.max_decode_packets = 500
app = Flask(__name__,
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER)
app.config["SECRET_KEY"] = "secret"
testmode=False
socketio = SocketIO(app,
                    engineio_logger=testmode)

CHATBOX_HOLD = False



def start_web_sources():
    """Function to start Flask server for OBS
    web sources."""

    @app.route("/chatbox")
    def tchat():
        """Function for the chatbox browser source."""

        return render_template("chat.html",
        BGColor = Variables.CHATBOXSETTINGS['bgcolor'],
        Fontsize = Variables.CHATBOXSETTINGS['FontSize'],
        Fontsource = Variables.CHATBOXSETTINGS['FontSource'],
        Fontcolor = Variables.CHATBOXSETTINGS['FontColor'],
        Fontname = Variables.CHATBOXSETTINGS['FontName'],
        BGOpacity = Variables.CHATBOXSETTINGS['opacity'])

    def refreshchatbox():
        """Function for checking list for updated
        chatbox source values."""
        global CHATBOX_HOLD
        while True:
            if Variables.CHATBOXSETTINGS['refresh'] == 'True':
                CHATBOX_HOLD = True
                socketio.emit('clear-chat')
                Variables.CHATBOXSETTINGS['refresh'] = 'False'
                CHATBOX_HOLD = False
            socketio.sleep(.1)

    def msgremer():
        """Function to check for removing chatbox messages."""
        Variables.CHATBOXSETTINGS['datalist'] = []
        while True:
            socketio.sleep(.1)
            if next(iter(Variables.CHATBOXSETTINGS['datalist'] or []), None) is not None:
                torem = []
                if range(len(Variables.CHATBOXSETTINGS['datalist'])) == 1:
                    msgstorem = Variables.CHATBOXSETTINGS['datalist'][0].split(',')
                    torem.append(msgstorem[2])
                    socketio.emit("removemessages", data=(torem))
                    Variables.CHATBOXSETTINGS['datalist'] = []
                    Variables.CHATBOXSETTINGS['remupdate'] = False
                    socketio.sleep(.1)
                else:
                    for i in Variables.CHATBOXSETTINGS['datalist']:
                        msgstorem = i.split(',')
                        torem.append(msgstorem[2])
                    socketio.emit("removemessages", data=(torem))
                    Variables.CHATBOXSETTINGS['datalist'] = []
                    Variables.CHATBOXSETTINGS['remupdate'] = False
                    socketio.sleep(.1)

    def escape(htmlstring):
        """Function to sanitize HTML strings. Returns cleaned string."""
        escapes = {'\"': '&quot;',
                '\'': '&#39;',
                '<': '&lt;',
                '>': '&gt;'}
        # This is done first to prevent escaping other escapes.
        htmlstring = htmlstring.replace('&', '&amp;')
        for seq, esc in escapes.items():
            socketio.sleep(.1)
            htmlstring = htmlstring.replace(seq, esc)
        return htmlstring

    def addmsg():
        """Function for adding messages to the chatbox"""
        Variables.CHATBOXSETTINGS['refresh'] = False
        Variables.CHATBOXSETTINGS['msgdict'] = []
        Variables.CHATBOXSETTINGS['addupdate'] = False
        while True:
            badges = ''
            fullmsg2 = ''
            socketio.sleep(.1)
            if Variables.CHATBOXSETTINGS['refresh']:
                socketio.emit("up-settings", data=(Variables.CHATBOXSETTINGS['FontSize'], Variables.CHATBOXSETTINGS['FontSource'],
                Variables.CHATBOXSETTINGS['FontColor'], Variables.CHATBOXSETTINGS['bgcolor'], Variables.CHATBOXSETTINGS['opacity']))
                Variables.CHATBOXSETTINGS['refresh'] = False
                socketio.sleep(.1)
            if Variables.CHATBOXSETTINGS['addupdate'] or next(iter(Variables.CHATBOXSETTINGS['msgdict'] or []), None) is not None:
                curmsg = Variables.CHATBOXSETTINGS['msgdict'].pop(0)
                if Variables.CHATBOXSETTINGS['disabledcmds'] == '1' and str(curmsg['message']).startswith('!'):
                    Variables.CHATBOXSETTINGS['addupdate'] = False
                    continue
                if curmsg['username'] in Variables.CHATBOXSETTINGS['disabledusers']:
                    Variables.CHATBOXSETTINGS['addupdate'] = False
                    continue
                else:
                    user = ''
                    badges2 = ''
                    emotes2 = ''
                    messages = ''
                    usercolor = ''
                    user = curmsg['username']
                    badges2 = curmsg['badges']
                    if badges2 is not None:
                        if Variables.CHATBOXSETTINGS['skipemotes'] is True:
                            badges = ''
                        else:
                            badges = TAPI.emotes.tcbadgeparser(badges2)
                    if badges2 is None:
                        badges = ''
                    messages = curmsg['message']
                    usercolor = curmsg['color']
                    emotes2 = curmsg['emotes']
                    if emotes2 is not None:
                        messages2 = messages
                        linklst = []
                        toreplem = []
                        emotelst = emotes2.split('/')
                        url, loc = map(list, zip(*(s.split(":") for s in emotelst)))
                        for i in url:
                            socketio.sleep(.1)
                            etest = requests.get(f"https://static-cdn.jtvnw.net/emoticons/v2/{i}/animated/light/1.0", timeout=10)
                            if str(etest) == '<Response [404]>':
                                linklst.append(str(f'<img src="https://static-cdn.jtvnw.net/emoticons/v2/{i}/static/light/1.0" width="'+str(int(Variables.CHATBOXSETTINGS['FontSize'])+8) + '" height="'+str(int(Variables.CHATBOXSETTINGS['FontSize'])+8) + '"/>'))
                            else:
                                linklst.append(str(f'<img src="https://static-cdn.jtvnw.net/emoticons/v2/{i}/animated/light/1.0" width="'+str(int(Variables.CHATBOXSETTINGS['FontSize'])+8) + '" height="'+str(int(Variables.CHATBOXSETTINGS['FontSize'])+8) + '"/>'))
                        for i in loc:
                            socketio.sleep(.1)
                            if "," in i:
                                z = i.split(',')
                                for q in z:
                                    splsli = q.split('-')
                                    begsl = splsli[:-1]
                                    endsl = splsli[-1:]
                                    if str(messages2[int(begsl[0]):int(endsl[0])+1]) not in toreplem:
                                        toreplem.append(str(messages2[int(begsl[0]):int(endsl[0])+1]))
                            else:
                                splsli = i.split('-')
                                begsl = splsli[:-1]
                                endsl = splsli[-1:]
                                toreplem.append(str(messages2[int(begsl[0]):int(endsl[0])+1]))

                        fullmsg2 = escape(htmlstring=messages)
                        for i, v in enumerate(toreplem):
                            socketio.sleep(.1)
                            # print(i, v)
                            fullmsg2 = fullmsg2.replace(v, str(linklst[i]))

                        fullmsg2 = TAPI.emotes.tcmessageparser(fullmsg2)
                    if emotes2 is None:
                        fullmsg2 = TAPI.emotes.tcmessageparser(escape(htmlstring=messages))
                        # fullmsg2 = TAPI.emotes.tcmessageparser(messages)

                    mid = curmsg['msgid']
                    data2 = '<span1 style="color:'+ usercolor + ';">'+ badges + user + '</span1>'
                    if curmsg['action'] == '1':
                        data3 = '<span style="color:'+ usercolor + ';";>' + ': ' +  fullmsg2 +'</span>'
                    else:
                        data3 = '<span style="color:'+ Variables.CHATBOXSETTINGS['FontColor'] + ';";>' + ': ' +  fullmsg2 +'</span>'
                    socketio.emit("new-message", data=(data2, data3, mid))
                    Variables.CHATBOXSETTINGS['addupdate'] = False
                socketio.sleep(.1)
            else:
                continue
    socketio.start_background_task(addmsg)
    socketio.start_background_task(msgremer)
    socketio.run(app, debug=False)


if __name__ == '__main__':
    start_web_sources()
