Update: tcmessageparser function in the TAPI file was updated to fix issues with some 7tv emotes not displaying


# Twitch-Streamchat

This is a very hastily pull out of the twitch chat browser source I created for a much more cohesive streaming tool and is likely to contain bugs. I'm also not the greatest programmer, so shield your eyes before digging in too deep.

In order to use the tool, you will need to replace any instance of "\<insert client id here\>", or "\<insert client secret here\>" with your Twitch application's client ID or secret. This is in both the Chatbot.py and TAPI.py files.
Next you will need to replace '\<insert your twitch user id here\>' in the TAPI.py file with your Twitch user ID.
After that you will want to replace '\<insert name of channel to connect to here\>' in the Variables file with the channel name you want to connect to. This must be in all lower case.
Last you will need to set the name for your bot in the Chatbot.py file within the __init__ function.

Then just launch from the chatbox.py file. You should see a browser window pop up to authenticate your Twitch account.
This is a quick and dirty setup for the streamchat, so you might need to restart the app to get it to connect after you initially authenticate as i have it on a 10 second wait at launch.
Lastly you should be met with a UI window that has various controls (font, font size, color, transparency, etc etc.).
At this point the chat should be working and can be added as a browser source to OBS with the url: 127.0.0.1:5000/chatbox
You can size the window in OBS to whatever you want, the chat should adjust automatically to fit.

Enjoy!

Misc:
The HTML template is located in the "templates" folder, if you wish to make any style adjustments.
Font files can be put into the /static/fonts directory if you wish to add custom fonts without manually adding them to the HTML template, and then selecting from the font list in the UI.
