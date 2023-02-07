import config


ADMIN = """
<u>**Only admin can use these commands :**</u>


/pause
» pause the current ongoing stream.

/resume
» resumed the pause stream.

/skip ᴏr /next
» skip the current ongoing stream.

/end ᴏʀ /stop
» end the current ongoing stream.

(✿◠‿◠)
"""


AUTH = """
<u>**Command to auth or unauth any user**</u>*

• Authorised user can skip, stop and pause stream without admin rights .

/auth [username or reply to a user] 
» add the user to authorized user list of group.

/unauth [username or reply to a user] 
» removes the user from authorized list of group.

/authusers 
» shows the list of authorized user of group.

(✿◠‿◠)
"""


PLAY = """
<u>**Commands to play songs :**</u>


/play <song-name/yt url/audio file>
» starts playing requeted song.

/queue
» shows the list of queued track .

/lyrics [sᴏɴɢ]
» shows the lyrics of searched song.

(✿◠‿◠)
"""


TOOLS = """
<u>**Some usefull tools :**</u>


/ping
» check if bot is alive or dead.

/start 
» starts the bot

/help 
» shows the help menu of the bot.

/stats
» show the server, latecy, speed and mongo-db of the bot.

/sudolist 
» shows the list of sudoers.


**Only for Sudoers :**

/speedtest 
» Check the speed, latecy and ms of bot.

(✿◠‿◠)
"""


OWNER = """
<u>**Commands that can only be used by owner of bot :**</u>


/chatlist
» list all the chat where bot is present.

/clean
» clean up tem directories.

/update 
» fetch update from repo.

/maintenance on
» enables the maintenance mode of bot.

/maintenance off
» disables the maintenance mode of bot.

/restart 
» restart the bot on your server.

(✿◠‿◠)
"""



SUDO = f"""
<u>**Command thatcan only be used by sudoers of bot :**</u>

/activevc
» show the list of active voice chat on the bot's server.

/gban [username or reply to a user]
» globally ban a user from all the chat bot served.

/ungban [username or reply to a user]
» globally unbanned a g-banned user.

/broadcast [message or reply to a message]
» broadcast the given message to all the served chats of the bot.

/broadcast_pin [message or reply to a message]
» broadcast the given message to all the served chats of the bot and pin that message also.

/joinassistant [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ]
» order the assistant to join that chat.

/leaveassistant [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ]
» order the assistant to leave that chat.

/leavebot [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ]
» order the bot to leave that chat.

{config.ASS_HANDLER[0]}approve [reply to a user's message] 
» approve the user to pm on your assitant account.

{config.ASS_HANDLER[0]}disapprove [reply to a user's message] 
» disapprove the user ot pm on your assistant account.

{config.ASS_HANDLER[0]}pfp [reply to a photo] 
» changes the pfp of assistant account.

{config.ASS_HANDLER[0]}bio [ᴛᴇxᴛ] 
» changes the bio of assistant account.

(✿◠‿◠)
"""
