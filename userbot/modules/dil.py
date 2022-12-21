# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_CHANNEL_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.dil ?(.*)")
@register(outgoing=True, pattern="^.lang ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    komut = event.pattern_match.group(1)
    if search(r"y[uü]kle|install", komut):
        await event.edit("`Dil faylı yüklənir... Zəhmət olmasa gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "secretjson")):
                return await event.edit("`Zəhmət olmasa, etibarlı "**SECRETJSON**" faylı təqdim edin!`")

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Zəhmət olmasa, etibarlı "**SECRETJSON**" faylı təqdim edin!`")

            await event.edit(f"`{dosya['LANGUAGE']}` `dili yüklənir...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            dosya = await reply.download_media(file="./userbot/language/")
            dosya = loads(open(dosya, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = dosya
            await event.edit(f"✅`{dosya['LANGUAGE']}` `dili uğurla quraşdırıldı!`\n\n**Hərəkətlərin qüvvəyə minməsi üçün botu yenidən başladın!**")
        else:
            await event.edit("**Zəhmət olmasa, dil faylına cavab verin!**")
    elif search(r"bilgi|info", komut):
        await event.edit("`Dil faylın məlumatı alınır... Zəhmət olmasa, gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "secretjson")):
                return await event.edit("`Zəhmət olmasa, etibarlı "**SECRETJSON**" faylı təqdim edin!`")

            dosya = await reply.download_media()

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Zəhmət olmasa, etibarlı "**SECRETJSON**" faylı təqdim edin!`")

            await event.edit(
                f"**Dil: **`{dosya['LANGUAGE']}`\n"
                f"**Dil Kodu: **`{dosya['LANGCODE']}`\n"
                f"**Tərcüməçi: **`{dosya['AUTHOR']}`\n"

                f"\n\n`Dil faylını quraşdırmaq üçün `.dil yükle` əmrindən istifadə edin.`"
            )
        else:
            await event.edit("**Zəhmət olmasa, dil faylına cavab verin!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil Kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Tərcüməçi: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\nRəsmi kanal: @TheSecretUserBot"
        )

CmdHelp('dil').add_command(
    'dil', None, 'Quraşdırdığınız dil haqqında məlumat verir.'
).add_command(
    'dil bilgi', None, 'Cavab verdiyiniz dil faylı haqqında məlumatı qaytarır.'
).add_command(
    'dil yükle', None, 'Cavab verdiyiniz dil faylını yükləyir.'
).add()
