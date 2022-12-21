import os
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil

load_dotenv("config.env")

# Bot günlükleri kurulumu:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @TheSecretUserBot - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - @TheSecretUserBot - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən azı python 3.6 versiyasına sahib olmalısınız."
              "Bir çox xüsusiyyət ondan asılıdır. Bot bağlanır.")
    quit(1)

CONFIG_CHECK = os.environ.get(
    "___________Xais_______Bu_____Setiri_____Silin__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Zəhmət olmasa, config.env faylından birinci teqdə göstərilən xətti çıxarın."
    )
    quit(1)

LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if not LANGUAGE in ["AZ", "DEFAULT"]:
    LOGS.info("Siz naməlum bir dil yazmısınız. Buna görə DEFAULT istifadə olunur.")
    LANGUAGE = "DEFAULT"
    
SECRET_VERSION = "1.0"

API_KEY = os.environ.get("API_KEY", "18482353")
API_HASH = os.environ.get("API_HASH", "9f7840b7015b359a49e142ce42decd71")

SILINEN_PLUGIN = {}
STRING_SESSION = os.environ.get("STRING_SESSION", None)

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0"))

BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

AUTO_PP = os.environ.get("AUTO_PP", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

BIO_PREFIX = os.environ.get("BIO_PREFIX", "@TheSecretUserBot | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///secret.db")

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

OTOMATIK_KATILMA = sb(os.environ.get("OTOMATIK_KATILMA", "True"))

PATTERNS = os.environ.get("PATTERNS", ".;!,")
WHITELIST = get('https://gitlab.com/Quiec/asen/-/raw/master/whitelist.json').json()

if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)


if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Braincheck faylı yoxdur, yüklənir...")

URL = 'https://raw.githubusercontent.com/quiec/databasescape/master/learning-data-root.check'
with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Fərdi xəta jurnalının işləməsi üçün konfiqurasiyadan BOTLOG_CHATID dəyişənini təyin etməlisiniz.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Giriş funksiyasının işləməsi üçün konfiqurasiyadan BOTLOG_CHATID dəyişənini təyin etməlisiniz..")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID qrupuna mesaj göndərmək səlahiyyəti yoxdur. "
            "Qrup ID-ni düzgün daxil etdiyinizi yoxlayın.")
        quit(1)
        
if not BOT_TOKEN == None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None

def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 2
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🚀 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("⬅️Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("lİləri", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]

with bot:
    if OTOMATIK_KATILMA:
        try:
            bot(JoinChannelRequest("@TheSecretUserBot"))
            bot(JoinChannelRequest("@TheSecretSupport"))
        except:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Salam, mən `@TheSecretUserBot`! Mən sahibimə (`@{me.username}`) kömək etmək üçün buradayam, ona görə də sizə kömək edə bilmərəm :/ Amma siz də Secret userbot qura bilərsiniz; ` @TheSecretUserBot kanalına baxın')
            else:
                await event.reply(f'`👑Secret Userbot İşləyir...`')

        @tgbot.on(InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@TheSecretUserBot":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Yalnız .help əmri ilə istifadə edin",
                    text=f"**👑**[Secret Userbot](https://t.me/TheSecretUserBot) __İşləyir...__\n\n**Yüklənmiş Modulların Sayı:** `{len(CMD_HELP)}`\n**Səyfə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl Yükləndi",
                    text=f"**Fayl uğurla {hissə[2]}-yə yükləndi!**\n\nYükleme zamanı: {parca[1][:3]} saniyə\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "@TheSecretUserBot",
                    text="""@TheSecretUserBot'u istifadə etməyə çalışın!
Hesabınızı bota çevirə və ondan istifadə edə bilərsiniz. Unutmayın ki, siz başqasının botunu idarə edə bilməzsiniz!""",
                    buttons=[
                        [custom.Button.url("👑Rəsmi Kanal", "https://t.me/TheSecretUserBot"), custom.Button.url(
                            "🚀Rəsmi Qrup", "https://t.me/TheSecretSupport")],
                        [custom.Button.url(
                            "🔍Plugin", "https://t.me/TheSecretPlugin")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌Hey! yazılarımı redaktə etməyə çalışmayın! Özünüzə @TheSecretUserBot yaradın.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**👑**[Secret Userbot](https://t.me/TheSecretUserBot) __İşləyir...__\n\n**Yüklənmiş Modulların Sayı:** `{len(CMD_HELP)}`\n**Səyfə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌Hey! yazılarımı redaktə etməyə çalışmayın! Özünüzə @TheSecretUserBot yaradın", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🚀 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌Bu modüle açıklama yazılmamış.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("⬅️Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗Fayl:** `{komut}`\n**🔢Əmrlər:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌Hey! yazılarımı redaktə etməyə çalışmayın! Özünüzə @TheSecretUserBot yaradın.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️Diqqət:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️Diqqət:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️Məlumat:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️nümunə:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("⬅️Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Botunuzda daxili dəstək deaktiv edilib. "
            "Aktivləşdirmək üçün bot nişanını təyin edin və botunuzda daxili rejimi aktivləşdirin. "
            "Bundan başqa problem olduğunu düşünürsünüzsə, bizimlə əlaqə saxlayın.."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "BOTLOG_CHATID mühit dəyişəni etibarlı obyekt deyil. "
            "Ətraf mühit dəyişənlərinizi / config.env faylını yoxlayın."
        )
        quit(1)


SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]
