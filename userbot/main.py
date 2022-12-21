import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, SECRET_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

AFKSTR = [
    "Mən indi tələsirəm, sonra mənə yaza bilərsən? Hər halda yenə gələcəm.",
    "Zəng etdiyiniz şəxs hazırda telefona cavab verə bilmir.`",
    "Mən bir neçə dəqiqəyə qayıdacağam. Amma gəlməsəm... daha gözləmə.",
    "Mən indi burada deyiləm, yəqin başqa yerdəyəm.",
]

UNAPPROVED_MSG = ("`👋Hey,` {mention}`! Bu bir bot. Endişelenme.\n\n`"
                  "`📢Sahibim sənə meşaj göndərməyə icazə verməyib. `"
                  "`⏳Xahiş edirəm sahibimin aktiv olmasını gözləyin, o, adətən meşajlari təsdiqləyir.\n\n`"
                  "`🆘Sahibimə 3 meşaj göndərdiyin zaman əngəllənəcəksən.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\n❌Xəta: Daxil edilən telefon nömrəsi yanlışdır' \
             '\n🔐İpucu: Ölkə kodundan istifadə edərək nömrənizi daxil edin' \
             '\nℹ️Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            Secretpy = re.search('\"\"\"SECRETPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Secretpy == None:
                Secretpy = Secretpy.group(0)
                for Satir in Secretpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # əmr = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, '🆘Bu plugin başqa yerdən yüklənib. Təsvir müəyyən edilməyib.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    asenabl = requests.get('https://gitlab.com/Quiec/asen/-/raw/master/asen.json').json()
    if idim in asenabl:
        bot.disconnect()

    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    GALERI = {}

    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`👑Secret Userbot İşləyir...`", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`👋Özünüzə yaxşı baxın mən çıxdım`", "pm": UNAPPROVED_MSG, "ban": "❌ {mention}`, Qadağan edildi!`", "mute": "🔇 {mention}`, Səssizə alındı!`", "approve": "🔓 {mention}`, Mənə mesaj göndərə bilərsən!`", "disapprove": "🔒 {mention}`, Daha mənə mesaj göndərə bilməzsən!`", "block": "🔒{mention}`, Bloklandın!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("Pluginlər yüklənir...")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin Artıq Quraşdırılıb " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`Yükləmə uğursuz oldu! plugində Xəta aşkar edildi.\n\n❌Xəta: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`ℹ️Pluginləri daimi etmək üçün PLUGIN_CHANNEL_ID təyin edin.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Secret Userbot İşləyir! "
          "Köməyə ehtiyacınız varsa, t.me/TheSecretSupport dəstək qrupumuza gəlin")
LOGS.info(f"Secret UserBot Versiyası: {SECRET_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
