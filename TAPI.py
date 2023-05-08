# pylint: disable=bad-option-value,line-too-long, too-many-lines, global-statement, invalid-name, bare-except, global-variable-not-assigned, missing-module-docstring, unused-argument

import sys
import threading
import time
from re import search

import requests
import Variables
from twitchAPI import EventSub, Twitch  # , helper, types
from twitchAPI.oauth import UserAuthenticator  # , refresh_access_token
# from twitchAPI.pubsub import PubSub
from twitchAPI.types import AuthScope

hookurl = ""
client_id = "<insert client id here>"
client_secret = "<insert client secret here>"
ngroktok = ""
streamer = ""
BTTVGLOBALS = []
BTTVUSER = []
SEVENTVGLOBALS = []
SEVENTVUSER = []
FFZUSER = []
TWITCHGLOBALS = []
TWITCHUSER = []
TCHANEMOTENAMES = []
TCHANEMOTEIDS = []
TCHANEMOTEANI = []
GTCHANEMOTENAMES = []
GTCHANEMOTEIDS = []
TCGLOBALBDG = []
TCUSERBDG = []
STREAMERTWITCHID = '<insert your twitch user id here>'

def set_client_info():
    """Sets global variables for client info."""

    global streamer
    streamer = Variables.STREAMER['streamer']

def token_gen():
    """Generates authentication and refresh tokens for Twitch's API.
    Stores tokens to reuse. Only triggered if stored tokens fail."""

    twitch = Twitch(client_id, client_secret)
    twitch.authenticate_app([])
    target_scope = [
        AuthScope.CHANNEL_READ_REDEMPTIONS,
        AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
        AuthScope.BITS_READ,
        AuthScope.CHANNEL_READ_HYPE_TRAIN,
    ]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    twitch.set_user_authentication(token, target_scope, refresh_token)
    Variables.TOKENS = {'auth': token, 'refresh': refresh_token}

def tokrefresh():
    """Starts a loop to keep twitch tokens refreshed. Stores updated tokens
    for future reuse."""

    global startflag
    while True:
        time.sleep(3600)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data1 = f"grant_type=refresh_token&refresh_token={Variables.TOKENS['refresh']}&client_id={client_id}&client_secret={client_secret}"
        response1 = requests.post('https://id.twitch.tv/oauth2/token', timeout=10, headers=headers, data=data1).json()
        Variables.TOKENS['auth'] = str(response1['access_token'])
        Variables.TOKENS['refresh'] = str(response1['refresh_token'])

class EmoteBuilder:
    """Class for parsing and building messages with emotes for browser sources."""
    def __init__(self):
        self.test = "test"

    def emotefetcher(self):
        """Function for fetching emote lists from various services."""
        livefetch = True
        emotes.twitchfetcher()
        while livefetch:
            emotes.bttvfetcher()
            emotes.seventvfetcher()
            emotes.ffzfetcher()
            time.sleep(300)

    def bttvfetcher(self):
        """Function for fetching BTTV emote list."""
        global BTTVGLOBALS
        global BTTVUSER
        try:
            globalemoteurl = "https://api.betterttv.net/3/cached/emotes/global"
            BTTVGLOBALS = requests.get(globalemoteurl, timeout=10).json()
            useremoteurl = f"https://api.betterttv.net/3/cached/users/twitch/{STREAMERTWITCHID}"
            userlink = requests.get(useremoteurl, timeout=10).json()
            BTTVUSER = userlink['channelEmotes'] + userlink['sharedEmotes']
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

    def seventvfetcher(self):
        """Function for fetching 7tv emote list."""
        global SEVENTVGLOBALS
        global SEVENTVUSER
        try:
            globalemoteurl = "https://api.7tv.app/v2/emotes/global"
            SEVENTVGLOBALS = requests.get(globalemoteurl, timeout=10).json()
            useremoteurl = "https://api.7tv.app/v2/users/marshbag12/emotes"
            SEVENTVUSER = requests.get(useremoteurl, timeout=10).json()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

    def ffzfetcher(self):
        """Function for fetching FFZ emote list."""
        global FFZUSER
        try:
            useremoteurl = f"https://api.betterttv.net/3/cached/frankerfacez/users/twitch/{STREAMERTWITCHID}"
            FFZUSER = requests.get(useremoteurl, timeout=10).json()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

    def twitchfetcher(self):
        """Function for fetching Twitch emotes."""
        global TWITCHGLOBALS
        global TWITCHUSER
        global TCHANEMOTENAMES
        global TCHANEMOTEIDS
        global TCHANEMOTEANI
        global GTCHANEMOTENAMES
        global GTCHANEMOTEIDS
        global TCGLOBALBDG
        global TCUSERBDG
        globalemoteurl = "https://api.twitch.tv/helix/chat/emotes/global"
        headers = {"Client-ID": f"{client_id}",
                "Authorization": "Bearer " + Variables.TOKENS['auth']}
        globalbadgeurl = "https://api.twitch.tv/helix/chat/badges/global"
        userbadgeurl = f"https://api.twitch.tv/helix/chat/badges?broadcaster_id={STREAMERTWITCHID}"
        TWITCHGLOBALS = requests.get(globalemoteurl, headers=headers, timeout=10).json()['data']
        TCGLOBALBDG = requests.get(globalbadgeurl, headers=headers, timeout=10).json()['data']
        TCUSERBDG = requests.get(userbadgeurl, headers=headers, timeout=10).json()['data']
        GTCHANEMOTENAMES = [i['name'] for i in TWITCHGLOBALS if 'name' in i]
        GTCHANEMOTEIDS = [i['id'] for i in TWITCHGLOBALS if 'name' in i]
    def bttvlinkgen(self, emoteid, size):
        """Function for building BTTV emote links."""
        emoteurl = f"https://cdn.betterttv.net/emote/{emoteid}/{size}x"
        return emoteurl

    def seventvlinkgen(self, emoteid, size):
        """Function for building 7tv emote links."""
        emoteurl = f"https://cdn.7tv.app/emote/{emoteid}/{size}x.webp"
        return emoteurl

    def ffzlinkgen(self, emoteid, size):
        """Function for building FFZ emote links."""
        emoteurl = f"https://cdn.betterttv.net/frankerfacez_emote/{emoteid}/{size}"
        return emoteurl

    def twitchlinkgen(self, emoteid, animated, theme_mode, size):
        """Function for building Twitch emote links."""
        emoteurl = f"https://static-cdn.jtvnw.net/emoticons/v2/{emoteid}/{animated}/{theme_mode}/{size}.0"
        return emoteurl

    def tcmessageparser(self, message):
        """Main function for parsing and replacing twitch chat emotes."""
        messageparse = message.split(' ')
        for i in messageparse:
            if any(not c.isalnum() for c in i):
                pass
            else:
                for e in BTTVGLOBALS:
                    if e['code'] == i:
                        emoteid = e['id']
                        emotelink = str(emotes.bttvlinkgen(emoteid, size='1'))
                        messageparse = ['<img src="' + emotelink + '"/>' if item == i else item for item in messageparse]
                        continue
                for e in BTTVUSER:
                    if e['code'] == i:
                        emoteid = e['id']
                        emotelink = str(emotes.bttvlinkgen(emoteid, size='1'))
                        messageparse = ['<img src="' + emotelink + '"/>' if item == i else item for item in messageparse]
                        continue
                if (match := search("'" +i+r"', 'images': {'1x': 'https://cdn.betterttv.net/frankerfacez_emote/[a-zA-Z0-9.\[\]\\`_\^\{\|\}-]{1,32}/1'", str(FFZUSER))):
                    msglength = len(i) + 67
                    emoteid = match.group(0)[msglength:-3]
                    emotelink = str(emotes.ffzlinkgen(emoteid, size='1'))
                    messageparse = ['<img src="' + emotelink + '"/>' if item == i else item for item in messageparse]
                    continue
                for e in SEVENTVGLOBALS:
                    if e['name'] == i:
                        emoteid = e['id']
                        emotelink = str(emotes.seventvlinkgen(emoteid, size='1'))
                        messageparse = ['<img src="' + emotelink + '"/>' if item == i else item for item in messageparse]
                        continue
                for e in SEVENTVUSER:
                    if e['name'] == i:
                        emoteid = e['id']
                        emotelink = str(emotes.seventvlinkgen(emoteid, size='1'))
                        messageparse = ['<img src="' + emotelink + '"/>' if item == i else item for item in messageparse]
                        continue
        newmessage = ' '.join(messageparse)
        return newmessage

    def tcbadgeparser(self, badge):
        """Function to add badge image links to chatbox source messages."""
        badgeparse = badge.split(',')
        for i in badgeparse:
            newbdg = i.split('/')
            bdgid = newbdg[:-1]
            bdgtype = newbdg[-1:]
            for x in TCUSERBDG:
                if x['set_id'] == bdgid[0]:
                    for z in x['versions']:
                        if z['id'] == bdgtype[0]:
                            emotelink = str(z['image_url_1x'])
                            badgeparse = ['<img src="' + emotelink + '"/> ' if item == i else item for item in badgeparse]#badgeparse2.replace(str(bdgid[0]) + r'/[0-9]', '<img src="' + emotelink + '" width="20" height="20"/>')
            for x in TCGLOBALBDG:
                if x['set_id'] == bdgid[0]:
                    for z in x['versions']:
                        if z['id'] == bdgtype[0]:
                            emotelink = str(z['image_url_1x'])
                            badgeparse = ['<img src="' + emotelink + '"/> ' if item == i else item for item in badgeparse]#badgeparse2.replace(str(bdgid[0]) + r'/[0-9]', '<img src="' + emotelink + '" width="20" height="20"/>')
        newbdgparse = ' '.join(badgeparse)
        return newbdgparse

emotes = EmoteBuilder()

def emote_fetcher():
    """Function to initialize emote fetching."""
    emotefetcher = threading.Thread(target=emotes.emotefetcher, daemon=True)
    emotefetcher.start()

def startup():
    """Loads stored tokens. Attempts to refresh stored tokens. If
    stored tokens fail to refresh, it generates new tokens.
    Initializes reverse proxy service. Starts Twitch webhook API."""

    set_client_info()
    token_gen()
    time.sleep(.2)
    TAPItokenrefresh = threading.Thread(target=tokrefresh, daemon=True)
    TAPItokenrefresh.start()
    emote_fetcher()
