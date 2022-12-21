from random import randint
from asyncio import sleep
from os import execl
import sys
import io
import sys
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("misc")

@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ . """
    await wannahelp.edit(LANG['SUPPORT_GROUP'])


CmdHelp('support').add_command(
    'support', None, 'Support Qrupun Göndərir.'
).add()
