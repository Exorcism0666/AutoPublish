import requests
import pathlib
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os, sys
urllib3.disable_warnings(InsecureRequestWarning)
import json
import bs4
import re

GH_TOKEN = sys.argv[1]

def report_existed(id: str, Version: str) -> None:
    print(f"{id}: {Version} has already existed, skip publishing")

def komac(path: str, debug: bool = False) -> pathlib.Path:
    Komac = pathlib.Path(path)/"komac.exe"
    if not debug:
        with open(Komac, "wb+") as f:
            file = requests.get("https://github.com/russellbanks/Komac/releases/download/nightly/komac-nightly-x86_64-pc-windows-msvc.exe", verify=False)
            f.write(file.content)
    return Komac

def command(komac: pathlib.Path, id: str, urls: str, version: str, token: str) -> str:
    Commands = "{} update --identifier {} --urls {} --version {} --submit --token {}".format(komac.__str__(), id, urls, version, token)
    return Commands

def clean_string(string: str, keywords: dict[str, str]) -> str:
    for k in keywords:
        string = string.replace(k, keywords[k])
    return string

def str_pop(string: str, index: int) -> str:
        i = list(string)
        i.pop(index)
        i = "".join(i)

        return i

def list_to_str(List: list) -> str:
    new = str(List)
    new = clean_string(new, {
         "[": "",
         "]": "",
         " ": "",
         "'": "",
         ",": " "
    })
    return new

def version_verify(version: str, id: str) -> bool:
    try:
        if len([v for v in requests.get(f"https://vedantmgoyal.vercel.app/api/winget-pkgs/versions/{id}").json()["Versions"] if v == version]) > 0:
            return False
        else:
            return True
    except BaseException:
        return True

def do_list(id: str, version: str, mode: str) -> bool | None:
    """
    Mode: write or verify
    """
    path = pathlib.Path(__file__).parents[0] / "config" / "list.json"
    with open(path, "r", encoding="utf-8") as f:
        try:
            JSON: dict[str, list[str]] = json.loads(f.read())
        except BaseException:
            JSON: dict[str, list[str]] = {}
        if id not in JSON:
            JSON[id] = []
        
        if mode == "write":
            if version not in JSON[id]:
                JSON[id].append(version)
            with open(path, "w+", encoding="utf-8") as w:
                w.write(json.dumps(JSON, indent=2, sort_keys=True))
        elif mode == "verify":
            if version in JSON[id]:
                return True
            else:
                return False
        else:
            raise Exception
 
def main() -> list[tuple[str, tuple[str, str, str]]]:
    Commands:list[tuple[str, tuple[str, str, str]]] = []
    debug = bool([each for each in sys.argv if each == "debug"])
    Komac = komac(pathlib.Path(__file__).parents[0], debug)
    Headers = [{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Authorization": f"Bearer {GH_TOKEN}"
    }]
    '''
# Add Peppy.Osu! to Update List
    id = "Peppy.Osu!"
    JSON = requests.get("https://api.github.com/repos/ppy/osu/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ppy/osu/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add HandBrake.HandBrake to Update List
    id = "HandBrake.HandBrake"
    JSON = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/HandBrake/HandBrake/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("blockmap" in each["browser_download_url"]) or ("sig" in each["browser_download_url"])) and (("arm64" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add SchildiChat.SchildiChat to Update List
    id = "SchildiChat.SchildiChat"
    JSON = requests.get("https://api.github.com/repos/SchildiChat/schildichat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SchildiChat/schildichat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add cinnyapp.cinny-desktop to Update List
    id = "cinnyapp.cinny-desktop"
    JSON = requests.get("https://api.github.com/repos/cinnyapp/cinny-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/cinnyapp/cinny-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add Tyrrrz.DiscordChatExporter.CLI to Update List
    id = "Tyrrrz.DiscordChatExporter.CLI"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".Cli.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Tyrrrz.DiscordChatExporter.GUI to Update List
    id = "Tyrrrz.DiscordChatExporter.GUI"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("ChatExporter.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add Tyrrrz.LightBulb to Update List
    id = "Tyrrrz.LightBulb"
    JSON = requests.get("https://api.github.com/repos/Tyrrrz/LightBulb/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tyrrrz/LightBulb/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add yt-dlp.yt-dlp to Update List
    id = "yt-dlp.yt-dlp"
    JSON = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not each["browser_download_url"].endswith("min.exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add yt-dlp.yt-dlp.nightly to Update List
    id = "yt-dlp.yt-dlp.nightly"
    JSON = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp-nightly-builds/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/yt-dlp/yt-dlp-nightly-builds/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not each["browser_download_url"].endswith("min.exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add Gyan.FFmpeg.Essentials to Update List
    id = "Gyan.FFmpeg.Essentials"
    JSON = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("essentials_build.zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Obsidian.Obsidian to Update List
    id = "Obsidian.Obsidian"
    JSON = requests.get("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].startswith("Obsidian.")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add defi.defi to Update List
    id = "defi.defi"
    JSON = requests.get("https://api.github.com/repos/BirthdayResearch/defichain-app/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/BirthdayResearch/defichain-app/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add OleguerLlopart.OpenComic to Update List
    id = "OleguerLlopart.OpenComic"
    JSON = requests.get("https://api.github.com/repos/ollm/OpenComic/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ollm/OpenComic/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("Portable" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add manosim.gitify to Update List
    id = "manosim.gitify"
    JSON = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    
    # Add dscalzi.HeliosLauncher to Update List
    id = "dscalzi.HeliosLauncher"
    JSON = requests.get("https://api.github.com/repos/dscalzi/HeliosLauncher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dscalzi/HeliosLauncher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add ChrisKlimas.Twine to Update List
    id = "ChrisKlimas.Twine"
    JSON = requests.get("https://api.github.com/repos/klembot/twinejs/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/klembot/twinejs/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DaCosySheeep.FactDownloader to Update List
    id = "DaCosySheeep.FactDownloader"
    JSON = requests.get("https://api.github.com/repos/DaCosySheeep/FactDownloader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DaCosySheeep/FactDownloader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add jcv8000.Codex to Update List
    id = "jcv8000.Codex"
    JSON = requests.get("https://api.github.com/repos/jcv8000/Codex/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jcv8000/Codex/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AivarAnnamaa.Thonny to Update List
    id = "AivarAnnamaa.Thonny"
    JSON = requests.get("https://api.github.com/repos/thonny/thonny/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/thonny/thonny/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("xxl" in each["browser_download_url"]) or ("py38" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Lauriethefish.QuestPatcher to Update List
    id = "Lauriethefish.QuestPatcher"
    JSON = requests.get("https://api.github.com/repos/Lauriethefish/QuestPatcher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Lauriethefish/QuestPatcher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AppbyTroye.KoodoReader to Update List
    id = "AppbyTroye.KoodoReader"
    JSON = requests.get("https://api.github.com/repos/troyeguo/koodo-reader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/troyeguo/koodo-reader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("blockmap" in each["browser_download_url"]) or ("Portable" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add clouDr-f2e.rubick to Update List
    id = "clouDr-f2e.rubick"
    JSON = requests.get("https://api.github.com/repos/rubickCenter/rubick/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rubickCenter/rubick/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"]) and (("x64" in each["browser_download_url"]) or ("ia32" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add IPFS.IPFS-Desktop to Update List
    id = "IPFS.IPFS-Desktop"
    JSON = requests.get("https://api.github.com/repos/ipfs/ipfs-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ipfs/ipfs-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add jurplel.qView to Update List
    id = "jurplel.qView"
    JSON = requests.get("https://api.github.com/repos/jurplel/qView/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jurplel/qView/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add YACReader.YACReader to Update List
    id = "YACReader.YACReader"
    JSON = requests.get("https://api.github.com/repos/YACReader/yacreader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/YACReader/yacreader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("winx64-7z.exe" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add KeePassXCTeam.KeePassXC to Update List
    id = "KeePassXCTeam.KeePassXC"
    JSON = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("msi" in each["browser_download_url"]) and not("sig" in each["browser_download_url"]) or (("-LegacyWindows.msi" in each["browser_download_url"]) or ("DIGEST" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add JanProchazka.dbgate to Update List
    id = "JanProchazka.dbgate"
    JSON = requests.get("https://api.github.com/repos/dbgate/dbgate/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dbgate/dbgate/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("latest" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add staniel359.muffon to Update List
    id = "staniel359.muffon"
    JSON = requests.get("https://api.github.com/repos/staniel359/muffon/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/staniel359/muffon/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DuongDieuPhap.ImageGlass to Update List
    id = "DuongDieuPhap.ImageGlass"
    JSON = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/d2phap/ImageGlass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add sebescudie.GammaLauncher to Update List
    id = "sebescudie.GammaLauncher"
    JSON = requests.get("https://api.github.com/repos/sebescudie/GammaLauncher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/sebescudie/GammaLauncher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Ruben2776.PicView to Update List
    id = "Ruben2776.PicView"
    JSON = requests.get("https://api.github.com/repos/Ruben2776/PicView/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ruben2776/PicView/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add DEVCOM.LuaJIT to Update List
    id = "DEVCOM.LuaJIT"
    JSON = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-luajit/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-luajit/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord.Canary to Update List
    id = "Vendicated.Vencord.Canary"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord.PTB to Update List
    id = "Vendicated.Vencord.PTB"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Vendicated.Vencord to Update List
    id = "Vendicated.Vencord"
    JSON = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Vencord/Installer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "VencordInstallerCli.exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add chylex.DiscordHistoryTracker to Update List
    id = "chylex.DiscordHistoryTracker"
    JSON = requests.get("https://api.github.com/repos/chylex/Discord-History-Tracker/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chylex/Discord-History-Tracker/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "win-x64.zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Ombrelin.PlexRichPresence to Update List
    id = "Ombrelin.PlexRichPresence"
    JSON = requests.get("https://api.github.com/repos/Ombrelin/plex-rich-presence/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ombrelin/plex-rich-presence/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add PurpleI2P.i2pd to Update List
    id = "PurpleI2P.i2pd"
    JSON = requests.get("https://api.github.com/repos/PurpleI2P/i2pd/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/PurpleI2P/i2pd/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Tribler.Tribler to Update List
    id = "Tribler.Tribler"
    JSON = requests.get("https://api.github.com/repos/Tribler/tribler/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Tribler/tribler/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Retroshare.Retroshare to Update List
    id = "Retroshare.Retroshare"
    JSON = requests.get("https://api.github.com/repos/RetroShare/RetroShare/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/RetroShare/RetroShare/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Fly-io.flyctl to Update List
    id = "Fly-io.flyctl"
    JSON = requests.get("https://api.github.com/repos/superfly/flyctl/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/superfly/flyctl/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add NextDNS.NextDNS.CLI to Update List
    id = "NextDNS.NextDNS.CLI"
    JSON = requests.get("https://api.github.com/repos/nextdns/nextdns/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nextdns/nextdns/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("armv5" in each["browser_download_url"]) or ("armv6" in each["browser_download_url"]) or ("armv7" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AdGuard.dnsproxy to Update List
    id = "AdGuard.dnsproxy"
    JSON = requests.get("https://api.github.com/repos/AdguardTeam/dnsproxy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AdguardTeam/dnsproxy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AdGuard.AdGuardHome to Update List
    id = "AdGuard.AdGuardHome"
    JSON = requests.get("https://api.github.com/repos/AdguardTeam/AdGuardHome/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AdguardTeam/AdGuardHome/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("darwin" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Genymobile.scrcpy to Update List
    id = "Genymobile.scrcpy"
    JSON = requests.get("https://api.github.com/repos/Genymobile/scrcpy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Genymobile/scrcpy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".zip" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Frontesque.scrcpy+ to Update List
    id = "Frontesque.scrcpy+"
    JSON = requests.get("https://api.github.com/repos/Frontesque/scrcpy-plus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Frontesque/scrcpy-plus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Barry-ran.QtScrcpy to Update List
    id = "Barry-ran.QtScrcpy"
    JSON = requests.get("https://api.github.com/repos/barry-ran/QtScrcpy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/barry-ran/QtScrcpy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("ubuntu" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Balena.Etcher to Update List
    id = "Balena.Etcher"
    JSON = requests.get("https://api.github.com/repos/balena-io/etcher/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/balena-io/etcher/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("portable" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Balena.BalenaCLI to Update List
    id = "Balena.BalenaCLI"
    JSON = requests.get("https://api.github.com/repos/balena-io/balena-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/balena-io/balena-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ".exe" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add GeekCorner.threema to Update List
    id = "GeekCorner.threema"
    JSON = requests.get("https://api.github.com/repos/GeekCornerGH/threema-for-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GeekCornerGH/threema-for-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "Threema-For-Desktop-setup" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add OnionShare.OnionShare to Update List
    id = "OnionShare.OnionShare"
    JSON = requests.get("https://api.github.com/repos/onionshare/onionshare/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/onionshare/onionshare/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add quotient-im.Quaternion to Update List
    id = "quotient-im.Quaternion"
    JSON = requests.get("https://api.github.com/repos/quotient-im/Quaternion/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/quotient-im/Quaternion/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add DoltHub.Dolt to Update List
    id = "DoltHub.Dolt"
    JSON = requests.get("https://api.github.com/repos/dolthub/dolt/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dolthub/dolt/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Armin2208.WindowsAutoNightMode to Update List
    id = "Armin2208.WindowsAutoNightMode"
    JSON = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    
   # Add Chocolatey.Chocolatey to Update List
    id = "Chocolatey.Chocolatey"
    JSON = requests.get("https://api.github.com/repos/chocolatey/choco/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chocolatey/choco/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add ChawyeHsu.Hok to Update List
    id = "ChawyeHsu.Hok"
    JSON = requests.get("https://api.github.com/repos/chawyehsu/hok/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/chawyehsu/hok/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("sha256" in each["browser_download_url"]) and (("aarch64" in each["browser_download_url"]) or ("i686" in each["browser_download_url"]) or ("x86_64" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add Ryujinx.Ryujinx to Update List
    id = "Ryujinx.Ryujinx"
    JSON = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("sdl2" in each["browser_download_url"]) or ("ava" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
   # Add Ryujinx.Ryujinx.Ava to Update List
    id = "Ryujinx.Ryujinx.Ava"
    JSON = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Ryujinx/release-channel-master/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and ("ava" in each["browser_download_url"]) and not("sdl2" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add kramo.Cartridges to Update List
    id = "kramo.Cartridges"
    JSON = requests.get("https://api.github.com/repos/kra-mo/cartridges/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kra-mo/cartridges/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add hikari-no-yume.touchHLE to Update List
    id = "hikari-no-yume.touchHLE"
    JSON = requests.get("https://api.github.com/repos/hikari-no-yume/touchHLE/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/hikari-no-yume/touchHLE/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("Windows_x86_64.zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add LIJI32.SameBoy to Update List
    id = "LIJI32.SameBoy"
    JSON = requests.get("https://api.github.com/repos/LIJI32/SameBoy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/LIJI32/SameBoy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("cocoa" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Windscribe.Windscribe to Update List
    id = "Windscribe.Windscribe"
    JSON = requests.get("https://api.github.com/repos/Windscribe/Desktop-App/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Windscribe/Desktop-App/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("arm64" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add TeXstudio.TeXstudio to Update List
    id = "TeXstudio.TeXstudio"
    JSON = requests.get("https://api.github.com/repos/texstudio-org/texstudio/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/texstudio-org/texstudio/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Aserto.DSLoad to Update List
    id = "Aserto.DSLoad"
    JSON = requests.get("https://api.github.com/repos/aserto-dev/ds-load/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/aserto-dev/ds-load/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("darwin" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Joplin.Joplin to Update List
    id = "Joplin.Joplin"
    JSON = requests.get("https://api.github.com/repos/laurent22/joplin/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/laurent22/joplin/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("Portable" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Status.Status to Update List
    id = "Status.Status"
    JSON = requests.get("https://api.github.com/repos/status-im/status-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/status-im/status-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add jendrikseipp.RedNotebook to Update List
    id = "jendrikseipp.RedNotebook"
    JSON = requests.get("https://api.github.com/repos/jendrikseipp/rednotebook/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jendrikseipp/rednotebook/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add moneymanagerex.moneymanagerex to Update List
    id = "moneymanagerex.moneymanagerex"
    JSON = requests.get("https://api.github.com/repos/moneymanagerex/moneymanagerex/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/moneymanagerex/moneymanagerex/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("win32" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add GoXLR-on-Linux.GoXLR-Utility to Update List
    id = "GoXLR-on-Linux.GoXLR-Utility"
    JSON = requests.get("https://api.github.com/repos/GoXLR-on-Linux/goxlr-utility/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GoXLR-on-Linux/goxlr-utility/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Hugo.Hugo to Update List
    id = "Hugo.Hugo"
    JSON = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("extended" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Hugo.Hugo.Extended to Update List
    id = "Hugo.Hugo.Extended"
    JSON = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and ("extended" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add tangshimin.MuJing to Update List
    id = "tangshimin.MuJing"
    JSON = requests.get("https://api.github.com/repos/tangshimin/MuJing/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/tangshimin/MuJing/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Alist.Alist to Update List
    id = "Alist.Alist"
    JSON = requests.get("https://api.github.com/repos/alist-org/alist/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/alist-org/alist/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("upx" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add dynobo.NormCap to Update List
    id = "dynobo.NormCap"
    JSON = requests.get("https://api.github.com/repos/dynobo/normcap/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dynobo/normcap/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Bruno.Bruno to Update List
    id = "Bruno.Bruno"
    JSON = requests.get("https://api.github.com/repos/usebruno/bruno/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/usebruno/bruno/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SoftFever.OrcaSlicer to Update List
    id = "SoftFever.OrcaSlicer"
    JSON = requests.get("https://api.github.com/repos/SoftFever/OrcaSlicer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SoftFever/OrcaSlicer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add IPEP.Scantailor-Experimental to Update List
    id = "IPEP.Scantailor-Experimental"
    JSON = requests.get("https://api.github.com/repos/ImageProcessing-ElectronicPublications/scantailor-experimental/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ImageProcessing-ElectronicPublications/scantailor-experimental/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("X86-64-Qt6" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add nzbget.nzbget to Update List
    id = "nzbget.nzbget"
    JSON = requests.get("https://api.github.com/repos/nzbgetcom/nzbget/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nzbgetcom/nzbget/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("debug" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add RustDesk.RustDesk to Update List
    id = "RustDesk.RustDesk"
    JSON = requests.get("https://api.github.com/repos/rustdesk/rustdesk/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rustdesk/rustdesk/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SagerNet.sing-box to Update List
    id = "SagerNet.sing-box"
    JSON = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("amd64v3" in each["browser_download_url"]) or ("universal" in each["browser_download_url"]) or ("legacy" in each["browser_download_url"])) and (("arm64" in each["browser_download_url"]) or ("amd64" in each["browser_download_url"]) or ("386" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gopass.gopass to Update List
    id = "gopass.gopass"
    JSON = requests.get("https://api.github.com/repos/gopasspw/gopass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gopasspw/gopass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gopass.gopass-jsonapi to Update List
    id = "gopass.gopass-jsonapi"
    JSON = requests.get("https://api.github.com/repos/gopasspw/gopass-jsonapi/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gopasspw/gopass-jsonapi/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("armv6" in each["browser_download_url"]) or ("armv7" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add AGSProjectTeam.AdventureGameStudio to Update List
    id = "AGSProjectTeam.AdventureGameStudio"
    JSON = requests.get("https://api.github.com/repos/adventuregamestudio/ags/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/adventuregamestudio/ags/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add TailwindLabs.TailwindCSS to Update List
    id = "TailwindLabs.TailwindCSS"
    JSON = requests.get("https://api.github.com/repos/tailwindlabs/tailwindcss/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/tailwindlabs/tailwindcss/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Alex313031.Thorium to Update List
    id = "Alex313031.Thorium"
    JSON = requests.get("https://api.github.com/repos/Alex313031/Thorium-Win/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Alex313031/Thorium-Win/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HTTPie.HTTPie to Update List
    id = "HTTPie.HTTPie"
    JSON = requests.get("https://api.github.com/repos/httpie/desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/httpie/desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add squalou.google-chat-linux to Update List
    id = "squalou.google-chat-linux"
    JSON = requests.get("https://api.github.com/repos/squalou/google-chat-linux/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/squalou/google-chat-linux/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add mikf.gallery-dl to Update List
    id = "mikf.gallery-dl"
    JSON = requests.get("https://api.github.com/repos/mikf/gallery-dl/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/mikf/gallery-dl/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("sig" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add houmain.keymapper to Update List
    id = "houmain.keymapper"
    JSON = requests.get("https://api.github.com/repos/houmain/keymapper/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/houmain/keymapper/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add printfn.fend to Update List
    id = "printfn.fend"
    JSON = requests.get("https://api.github.com/repos/printfn/fend/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/printfn/fend/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if "windows" in each["browser_download_url"]]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add gaphor.gaphor to Update List
    id = "gaphor.gaphor"
    JSON = requests.get("https://api.github.com/repos/gaphor/gaphor/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gaphor/gaphor/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("portable" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add oxen-io.lokinet to Update List
    id = "oxen-io.lokinet"
    JSON = requests.get("https://api.github.com/repos/oxen-io/lokinet/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/oxen-io/lokinet/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HiroshibaKazuyuki.VOICEVOX to Update List
    id = "HiroshibaKazuyuki.VOICEVOX"
    JSON = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("cpu" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add HiroshibaKazuyuki.VOICEVOX.CPU to Update List
    id = "HiroshibaKazuyuki.VOICEVOX.CPU"
    JSON = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/VOICEVOX/voicevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX to Update List
    id = "y-chan.SHAREVOX"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("cpu" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("nvidia" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX.CPU to Update List
    id = "y-chan.SHAREVOX.CPU"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("nvidia" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add y-chan.SHAREVOX.NVIDIA to Update List
    id = "y-chan.SHAREVOX.NVIDIA"
    JSON = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SHAREVOX/sharevox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("directml" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("cpu" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SpikeHD.Dorion to Update List
    id = "SpikeHD.Dorion"
    JSON = requests.get("https://api.github.com/repos/SpikeHD/Dorion/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SpikeHD/Dorion/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add XmirrorSecurity.OpenSCA-cli to Update List
    id = "XmirrorSecurity.OpenSCA-cli"
    JSON = requests.get("https://api.github.com/repos/XmirrorSecurity/OpenSCA-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/XmirrorSecurity/OpenSCA-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("sha256" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add DEVCOM.JMeter to Update List
    id = "DEVCOM.JMeter"
    JSON = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-jmeter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DevelopersCommunity/cmake-jmeter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Nethermind.Nethermind to Update List
    id = "Nethermind.Nethermind"
    JSON = requests.get("https://api.github.com/repos/NethermindEth/nethermind/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/NethermindEth/nethermind/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("assemblies" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add lucasg.Dependencies to Update List
    id = "lucasg.Dependencies"
    JSON = requests.get("https://api.github.com/repos/lucasg/Dependencies/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/lucasg/Dependencies/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("x64" in each["browser_download_url"]) or ("Debug" in each["browser_download_url"]) or ("without" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add PhapDieuDuong.ExifGlass to Update List
    id = "PhapDieuDuong.ExifGlass"
    JSON = requests.get("https://api.github.com/repos/d2phap/ExifGlass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/d2phap/ExifGlass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add GAM-Team.GotYourBack to Update List
    id = "GAM-Team.GotYourBack"
    JSON = requests.get("https://api.github.com/repos/GAM-team/got-your-back/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/GAM-team/got-your-back/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
   # Add taers232c.GAMADV-XTD3 to Update List
    id = "taers232c.GAMADV-XTD3"
    JSON = requests.get("https://api.github.com/repos/taers232c/GAMADV-XTD3/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/taers232c/GAMADV-XTD3/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add Aserto.Topaz to Update List
    id = "Aserto.Topaz"
    JSON = requests.get("https://api.github.com/repos/aserto-dev/topaz/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/aserto-dev/topaz/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("linux" in each["browser_download_url"]) or ("darwin" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add UniversalMediaServer.UniversalMediaServer to Update List
    id = "UniversalMediaServer.UniversalMediaServer"
    JSON = requests.get("https://api.github.com/repos/UniversalMediaServer/UniversalMediaServer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/UniversalMediaServer/UniversalMediaServer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
   # Add Canonical.Multipass to Update List
    id = "Canonical.Multipass"
    JSON = requests.get("https://api.github.com/repos/canonical/multipass/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/canonical/multipass/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
   # Add AppFlowy.AppFlowy to Update List
    id = "AppFlowy.AppFlowy"
    JSON = requests.get("https://api.github.com/repos/AppFlowy-IO/AppFlowy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AppFlowy-IO/AppFlowy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add errata-ai.Vale to Update List
    id = "errata-ai.Vale"
    JSON = requests.get("https://api.github.com/repos/errata-ai/vale/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/errata-ai/vale/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add Jubler.App to Update List
    id = "Jubler.App"
    JSON = requests.get("https://api.github.com/repos/teras/Jubler/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/teras/Jubler/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add Task.Task to Update List
    id = "Task.Task"
    JSON = requests.get("https://api.github.com/repos/go-task/task/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/go-task/task/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and (("arm64" in each["browser_download_url"]) or ("amd64" in each["browser_download_url"]) or ("386" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add martinrotter.RSSGuard to Update List
    id = "martinrotter.RSSGuard"
    JSON = requests.get("https://api.github.com/repos/martinrotter/rssguard/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/martinrotter/rssguard/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("lite" in each["browser_download_url"]) or ("win7" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
   # Add Stoplight.Prism to Update List
    id = "Stoplight.Prism"
    JSON = requests.get("https://api.github.com/repos/stoplightio/prism/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/stoplightio/prism/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add creativeprojects.resticprofile to Update List
    id = "creativeprojects.resticprofile"
    JSON = requests.get("https://api.github.com/repos/creativeprojects/resticprofile/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/creativeprojects/resticprofile/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("darwin" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SagerNet.sing-box to Update List
    id = "SagerNet.sing-box"
    JSON = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/SagerNet/sing-box/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("universal" in each["browser_download_url"]) or ("legacy" in each["browser_download_url"]) or ("v3" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add lycheeverse.lychee to Update List
    id = "lycheeverse.lychee"
    JSON = requests.get("https://api.github.com/repos/lycheeverse/lychee/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/lycheeverse/lychee/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add SMPlayer.SMPlayer to Update List
    id = "SMPlayer.SMPlayer"
    JSON = requests.get("https://api.github.com/repos/smplayer-dev/smplayer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/smplayer-dev/smplayer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("x64-qt5.6" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add YS-L.csvlens to Update List
    id = "YS-L.csvlens"
    JSON = requests.get("https://api.github.com/repos/YS-L/csvlens/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/YS-L/csvlens/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("sha256" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add z-------------.cpod to Update List
    id = "z-------------.cpod"
    JSON = requests.get("https://api.github.com/repos/z-------------/CPod/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/z-------------/CPod/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Stripe.StripeCli to Update List
    id = "Stripe.StripeCli"
    JSON = requests.get("https://api.github.com/repos/stripe/stripe-cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/stripe/stripe-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("i386" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add beekeeper-studio.beekeeper-studio to Update List
    id = "beekeeper-studio.beekeeper-studio"
    JSON = requests.get("https://api.github.com/repos/beekeeper-studio/beekeeper-studio/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/beekeeper-studio/beekeeper-studio/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("portable" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add AsciidocFX.AsciidocFX to Update List
    id = "AsciidocFX.AsciidocFX"
    JSON = requests.get("https://api.github.com/repos/asciidocfx/AsciidocFX/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/asciidocfx/AsciidocFX/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add BookStairs.bookhunter to Update List
    id = "BookStairs.bookhunter"
    JSON = requests.get("https://api.github.com/repos/bookstairs/bookhunter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/bookstairs/bookhunter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Ablaze.Floorp to Update List
    id = "Ablaze.Floorp"
    JSON = requests.get("https://api.github.com/repos/Floorp-Projects/Floorp/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Floorp-Projects/Floorp/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("stub" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Wilfred.difftastic to Update List
    id = "Wilfred.difftastic"
    JSON = requests.get("https://api.github.com/repos/Wilfred/difftastic/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Wilfred/difftastic/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Stretchly.Stretchly to Update List
    id = "Stretchly.Stretchly"
    JSON = requests.get("https://api.github.com/repos/hovancik/stretchly/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/hovancik/stretchly/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Streetwriters.Notesnook to Update List
    id = "Streetwriters.Notesnook"
    JSON = requests.get("https://api.github.com/repos/streetwriters/notesnook/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/streetwriters/notesnook/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"]) and (("arm64" in each["browser_download_url"]) or ("x64" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Logseq.Logseq to Update List
    id = "Logseq.Logseq"
    JSON = requests.get("https://api.github.com/repos/logseq/logseq/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/logseq/logseq/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Transmission.Transmission to Update List
    id = "Transmission.Transmission"
    JSON = requests.get("https://api.github.com/repos/transmission/transmission/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/transmission/transmission/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("msi" in each["browser_download_url"]) and (("qt5-x86" in each["browser_download_url"]) or ("qt5-x64" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add BiglySoftware.BiglyBT to Update List
    id = "BiglySoftware.BiglyBT"
    JSON = requests.get("https://api.github.com/repos/BiglySoftware/BiglyBT/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/BiglySoftware/BiglyBT/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not(("Java" in each["browser_download_url"]) or ("J8" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add szTheory.exifcleaner to Update List
    id = "szTheory.exifcleaner"
    JSON = requests.get("https://api.github.com/repos/szTheory/exifcleaner/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/szTheory/exifcleaner/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and ("Setup" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add qarmin.czkawka.cli to Update List
    id = "qarmin.czkawka.cli"
    JSON = requests.get("https://api.github.com/repos/qarmin/czkawka/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/qarmin/czkawka/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Syncthing.Syncthing to Update List
    id = "Syncthing.Syncthing"
    JSON = requests.get("https://api.github.com/repos/syncthing/syncthing/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/syncthing/syncthing/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("macos" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add EvanSu.Picocrypt to Update List
    id = "EvanSu.Picocrypt"
    JSON = requests.get("https://api.github.com/repos/HACKERALERT/Picocrypt/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/HACKERALERT/Picocrypt/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("Installer.exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add DNSCrypt.dnscrypt-proxy to Update List
    id = "DNSCrypt.dnscrypt-proxy"
    JSON = requests.get("https://api.github.com/repos/DNSCrypt/dnscrypt-proxy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DNSCrypt/dnscrypt-proxy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not(("android" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("minisig" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Oxen.Session to Update List
    id = "Oxen.Session"
    JSON = requests.get("https://api.github.com/repos/oxen-io/session-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/oxen-io/session-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add deltachat.deltachat to Update List
    id = "deltachat.deltachat"
    JSON = requests.get("https://api.github.com/repos/deltachat/deltachat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/deltachat/deltachat-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and ("Setup" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add uTox.uTox to Update List
    id = "uTox.uTox"
    JSON = requests.get("https://api.github.com/repos/uTox/uTox/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/uTox/uTox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("asc" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add RocketChat.RocketChat to Update List
    id = "RocketChat.RocketChat"
    JSON = requests.get("https://api.github.com/repos/RocketChat/Rocket.Chat.Electron/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/RocketChat/Rocket.Chat.Electron/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and ("x64" in each["browser_download_url"]) and not(("ia32" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Jitsi.Meet to Update List
    id = "Jitsi.Meet"
    JSON = requests.get("https://api.github.com/repos/jitsi/jitsi-meet-electron/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jitsi/jitsi-meet-electron/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Bisq.Bisq to Update List
    id = "Bisq.Bisq"
    JSON = requests.get("https://api.github.com/repos/bisq-network/bisq/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/bisq-network/bisq/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("asc" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add BinanceTech.Binance to Update List
    id = "BinanceTech.Binance"
    JSON = requests.get("https://api.github.com/repos/binance/desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/binance/desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add MullvadVPN.MullvadBrowser to Update List
    id = "MullvadVPN.MullvadBrowser"
    JSON = requests.get("https://api.github.com/repos/mullvad/mullvad-browser/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/mullvad/mullvad-browser/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("asc" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add MysteriumNetwork.Mysterium to Update List
    id = "MysteriumNetwork.Mysterium"
    JSON = requests.get("https://api.github.com/repos/mysteriumnetwork/mysterium-vpn-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/mysteriumnetwork/mysterium-vpn-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Meta.Zstandard to Update List
    id = "Meta.Zstandard"
    JSON = requests.get("https://api.github.com/repos/facebook/zstd/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/facebook/zstd/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Sonosaurus.SonoBus to Update List
    id = "Sonosaurus.SonoBus"
    JSON = requests.get("https://api.github.com/repos/sonosaurus/sonobus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/sonosaurus/sonobus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add YggdrasilNetwork.Yggdrasil to Update List
    id = "YggdrasilNetwork.Yggdrasil"
    JSON = requests.get("https://api.github.com/repos/yggdrasil-network/yggdrasil-go/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/yggdrasil-network/yggdrasil-go/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add StandardNotes.StandardNotes to Update List
    id = "StandardNotes.StandardNotes"
    JSON = requests.get("https://api.github.com/repos/standardnotes/app/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.sub(r'[^\d.]', '', requests.get("https://api.github.com/repos/standardnotes/app/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"])
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and (("ia32" in each["browser_download_url"]) or ("x64" in each["browser_download_url"])) and not("blockmap" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add stakira.OpenUTAU to Update List
    id = "stakira.OpenUTAU"
    JSON = requests.get("https://api.github.com/repos/stakira/OpenUtau/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.sub(r'[^\d.]', '', requests.get("https://api.github.com/repos/stakira/OpenUtau/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"])
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add RaspberryPiFoundation.RaspberryPiImager to Update List
    id = "RaspberryPiFoundation.RaspberryPiImager"
    JSON = requests.get("https://api.github.com/repos/raspberrypi/rpi-imager/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/raspberrypi/rpi-imager/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add K8stooling.Kubazulo to Update List
    id = "K8stooling.Kubazulo"
    JSON = requests.get("https://api.github.com/repos/k8stooling/kubazulo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/k8stooling/kubazulo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Speek.Speek to Update List
    id = "Speek.Speek"
    JSON = requests.get("https://api.github.com/repos/Speek-App/Speek/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.sub(r'[^\d.]', '', requests.get("https://api.github.com/repos/Speek-App/Speek/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"])
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Hydrogen-Music.Hydrogen to Update List
    id = "Hydrogen-Music.Hydrogen"
    JSON = requests.get("https://api.github.com/repos/hydrogen-music/hydrogen/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/hydrogen-music/hydrogen/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add ElectronCommunity.ElectronFiddle to Update List
    id = "ElectronCommunity.ElectronFiddle"
    JSON = requests.get("https://api.github.com/repos/electron/fiddle/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/electron/fiddle/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add win32ss.Supermium to Update List
    id = "win32ss.Supermium"
    JSON = requests.get("https://api.github.com/repos/win32ss/supermium/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/win32ss/supermium/releases/latest", verify=False, headers=Headers[1]).json()["name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add OpenRocket.OpenRocket to Update List
    id = "OpenRocket.OpenRocket"
    JSON = requests.get("https://api.github.com/repos/openrocket/openrocket/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.sub(r'[^\d.]', '', requests.get("https://api.github.com/repos/openrocket/openrocket/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"])
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add GnuCash.GnuCash to Update List
    id = "GnuCash.GnuCash"
    JSON = requests.get("https://api.github.com/repos/Gnucash/gnucash/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Gnucash/gnucash/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add JohnMacFarlane.Pandoc to Update List
    id = "JohnMacFarlane.Pandoc"
    JSON = requests.get("https://api.github.com/repos/jgm/pandoc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jgm/pandoc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Natron.Natron to Update List
    id = "Natron.Natron"
    JSON = requests.get("https://api.github.com/repos/NatronGitHub/Natron/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/NatronGitHub/Natron/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and not("unit" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add JeremyHu.Dust3D to Update List
    id = "JeremyHu.Dust3D"
    JSON = requests.get("https://api.github.com/repos/huxingyi/dust3d/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/huxingyi/dust3d/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add RandyHollines.Objeck to Update List
    id = "RandyHollines.Objeck"
    JSON = requests.get("https://api.github.com/repos/objeck/objeck-lang/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/objeck/objeck-lang/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add Meltytech.Shotcut to Update List
    id = "Meltytech.Shotcut"
    JSON = requests.get("https://api.github.com/repos/mltframework/shotcut/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/mltframework/shotcut/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add ossia.score to Update List
    id = "ossia.score"
    JSON = requests.get("https://api.github.com/repos/ossia/score/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ossia/score/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add FreeCAD.FreeCAD to Update List
    id = "FreeCAD.FreeCAD"
    JSON = requests.get("https://api.github.com/repos/FreeCAD/FreeCAD/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/FreeCAD/FreeCAD/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

    # Add InkStitch.InkStitch to Update List
    id = "InkStitch.InkStitch"
    JSON = requests.get("https://api.github.com/repos/inkstitch/inkstitch/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/inkstitch/inkstitch/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add stakira.OpenUTAU to Update List
    id = "stakira.OpenUTAU"
    JSON = requests.get("https://api.github.com/repos/stakira/OpenUtau/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/stakira/OpenUtau/releases/latest", verify=False, headers=Headers[1]).json()["name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith((".zip", ".exe"))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Nextcloud.NextcloudDesktop to Update List
    id = "Nextcloud.NextcloudDesktop"
    JSON = requests.get("https://api.github.com/repos/nextcloud-releases/desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nextcloud-releases/desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Armin2208.WindowsAutoNightMode to Update List
    id = "Armin2208.WindowsAutoNightMode"
    JSON = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AutoDarkMode/Windows-Auto-Night-Mode/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add keif888.SSISMHash to Update List
    id = "keif888.SSISMHash"
    JSON = requests.get("https://api.github.com/repos/keif888/SSISMHash/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/keif888/SSISMHash/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add f4exb.sdrangel to Update List
    id = "f4exb.sdrangel"
    JSON = requests.get("https://api.github.com/repos/f4exb/sdrangel/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/f4exb/sdrangel/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add foldynl.QLog to Update List
    id = "foldynl.QLog"
    JSON = requests.get("https://api.github.com/repos/foldynl/QLog/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/foldynl/QLog/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add alexx2000.DoubleCommander to Update List
    id = "alexx2000.DoubleCommander"
    JSON = requests.get("https://api.github.com/repos/doublecmd/doublecmd/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/doublecmd/doublecmd/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add divVerent.AAAAXY to Update List
    id = "divVerent.AAAAXY"
    JSON = requests.get("https://api.github.com/repos/divVerent/aaaaxy/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/divVerent/aaaaxy/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and (("386" in each["browser_download_url"]) or ("amd64" in each["browser_download_url"])) and not("linux" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Microsoft.PerfView to Update List
    id = "Microsoft.PerfView"
    JSON = requests.get("https://api.github.com/repos/microsoft/perfview/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/perfview/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add Google.Brotli to Update List
    id = "Google.Brotli"
    JSON = requests.get("https://api.github.com/repos/google/brotli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/google/brotli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and ("static" in each["browser_download_url"]) and not("dynamic" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add developersu.ns-usbloader to Update List
    id = "developersu.ns-usbloader"
    JSON = requests.get("https://api.github.com/repos/developersu/ns-usbloader/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/developersu/ns-usbloader/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and not("legacy" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add AssetRipper.AssetRipper to Update List
    id = "AssetRipper.AssetRipper"
    JSON = requests.get("https://api.github.com/repos/AssetRipper/AssetRipper/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AssetRipper/AssetRipper/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("zip" in each["browser_download_url"]) and ("win" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

   # Add soopercool101.BrawlCrate to Update List
    id = "soopercool101.BrawlCrate"
    JSON = requests.get("https://api.github.com/repos/soopercool101/BrawlCrate/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/soopercool101/BrawlCrate/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add GitHub.Atom to Update List
    id = "GitHub.Atom"
    JSON = requests.get("https://api.github.com/repos/atom/atom/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/atom/atom/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if ("exe" in each["browser_download_url"]) and ("x64" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add GitHub.GitLFS to Update List
    id = "GitHub.GitLFS"
    JSON = requests.get("https://api.github.com/repos/git-lfs/git-lfs/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/git-lfs/git-lfs/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Rufus.Rufus to Update List
    id = "Rufus.Rufus"
    JSON = requests.get("https://api.github.com/repos/pbatard/rufus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/pbatard/rufus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kopia.KopiaUI to Update List
    id = "Kopia.KopiaUI"
    JSON = requests.get("https://api.github.com/repos/kopia/kopia/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kopia/kopia/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kitware.CMake to Update List
    id = "Kitware.CMake"
    JSON = requests.get("https://api.github.com/repos/Kitware/CMake/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Kitware/CMake/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add dnGrep.dnGrep to Update List
    id = "dnGrep.dnGrep"
    JSON = requests.get("https://api.github.com/repos/dnGrep/dnGrep/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dnGrep/dnGrep/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Audacity.Audacity to Update List
    id = "Audacity.Audacity"
    JSON = requests.get("https://api.github.com/repos/audacity/audacity/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/audacity/audacity/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kubernetes.minikube to Update List
    id = "Kubernetes.minikube"
    JSON = requests.get("https://api.github.com/repos/kubernetes/minikube/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kubernetes/minikube/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add AutoHotkey.AutoHotkey to Update List
    id = "AutoHotkey.AutoHotkey"
    JSON = requests.get("https://api.github.com/repos/AutoHotkey/AutoHotkey/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/AutoHotkey/AutoHotkey/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.Azure.StorageExplorer to Update List
    id = "Microsoft.Azure.StorageExplorer"
    JSON = requests.get("https://api.github.com/repos/microsoft/AzureStorageExplorer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/AzureStorageExplorer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add RedHat.Podman-Desktop to Update List
    id = "RedHat.Podman-Desktop"
    JSON = requests.get("https://api.github.com/repos/containers/podman-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/containers/podman-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith("setup.exe") and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add dotPDNLLC.paintdotnet to Update List
    id = "dotPDNLLC.paintdotnet"
    JSON = requests.get("https://api.github.com/repos/paintdotnet/release/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/paintdotnet/release/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip") and not(("winmsi" in each["browser_download_url"]) or ("portable" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Ditto.Ditto to Update List
    id = "Ditto.Ditto"
    JSON = requests.get("https://api.github.com/repos/sabrogden/Ditto/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/sabrogden/Ditto/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Upscayl.Upscayl to Update List
    id = "Upscayl.Upscayl"
    JSON = requests.get("https://api.github.com/repos/upscayl/upscayl/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/upscayl/upscayl/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add nomacs.nomacs to Update List
    id = "nomacs.nomacs"
    JSON = requests.get("https://api.github.com/repos/nomacs/nomacs/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/nomacs/nomacs/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith((".msi", ".exe"))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add PDFsam.PDFsam to Update List
    id = "PDFsam.PDFsam"
    JSON = requests.get("https://api.github.com/repos/torakiki/pdfsam/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/torakiki/pdfsam/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi") and not("asc" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add manosim.gitify to Update List
    id = "manosim.gitify"
    JSON = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gitify-app/gitify/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add WinMerge.WinMerge to Update List
    id = "WinMerge.WinMerge"
    JSON = requests.get("https://api.github.com/repos/WinMerge/winmerge/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/WinMerge/winmerge/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add ShareX.ShareX to Update List
    id = "ShareX.ShareX"
    JSON = requests.get("https://api.github.com/repos/ShareX/ShareX/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ShareX/ShareX/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add DaxStudio.DaxStudio to Update List
    id = "DaxStudio.DaxStudio"
    JSON = requests.get("https://api.github.com/repos/DaxStudio/DaxStudio/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/DaxStudio/DaxStudio/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Gephi.Gephi to Update List
    id = "Gephi.Gephi"
    JSON = requests.get("https://api.github.com/repos/gephi/gephi/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/gephi/gephi/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("x32" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Giorgiotani.Peazip to Update List
    id = "Giorgiotani.Peazip"
    JSON = requests.get("https://api.github.com/repos/peazip/PeaZip/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/peazip/PeaZip/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add electerm.electerm to Update List
    id = "electerm.electerm"
    JSON = requests.get("https://api.github.com/repos/electerm/electerm/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/electerm/electerm/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("blockmap" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Eigenmiao.Rickrack to Update List
    id = "Eigenmiao.Rickrack"
    JSON = requests.get("https://api.github.com/repos/eigenmiao/Rickrack/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/eigenmiao/Rickrack/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("zh" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Kubernetes.kwok to Update List
    id = "Kubernetes.kwok"
    JSON = requests.get("https://api.github.com/repos/kubernetes-sigs/kwok/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kubernetes-sigs/kwok/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("kwokctl" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Waterfox.Waterfox to Update List
    id = "Waterfox.Waterfox"
    Version = requests.get("https://api.github.com/repos/WaterfoxCo/Waterfox/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [f"https://cdn1.waterfox.net/waterfox/releases/{Version}/WINNT_x86_64/Waterfox%20Setup%20{Version}.exe"]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add MiXXX.MiXXX to Update List
    id = "MiXXX.MiXXX"
    Version = requests.get("https://api.github.com/repos/mixxxdj/mixxx/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [f"https://downloads.mixxx.org/releases/{Version}/mixxx-{Version}-win64.msi"]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add NLnetLabs.Unbound to Update List
    id = "NLnetLabs.Unbound"
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/NLnetLabs/unbound/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [f"https://nlnetlabs.nl/downloads/unbound/unbound_setup_{Version}.exe"]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add commetchat.commet to Update List
    id = "commetchat.commet"
    Version = requests.get("https://api.github.com/repos/commetchat/commet/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [f"https://builds.commet.chat/builds/{Version}/commet-windows.zip"]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add Safing.Portmaster to Update List
    id = "Safing.Portmaster"
    Version = requests.get("https://api.github.com/repos/safing/portmaster/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [f"https://updates.safing.io/latest/windows_amd64/packages/portmaster-installer.exe"]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add Microsoft.AzureCLI to Update List
    id = "Microsoft.AzureCLI"
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/Azure/azure-cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [
    f"https://azcliprod.azureedge.net/msi/azure-cli-{Version}.msi",
    f"https://azcliprod.azureedge.net/msi/azure-cli-{Version}-x64.msi"]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add Microsoft.Bicep to Update List
    id = "Microsoft.Bicep"
    JSON = requests.get("https://api.github.com/repos/Azure/bicep/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Azure/bicep/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and ("setup" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.BotFrameworkComposerto Update List
    id = "Microsoft.BotFrameworkComposer"
    JSON = requests.get("https://api.github.com/repos/microsoft/BotFramework-Composer/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/BotFramework-Composer/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.BotFrameworkEmulator to Update List
    id = "Microsoft.BotFrameworkEmulator"
    JSON = requests.get("https://api.github.com/repos/microsoft/BotFramework-Emulator/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/BotFramework-Emulator/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.PowerToys to Update List
    id = "Microsoft.PowerToys"
    JSON = requests.get("https://api.github.com/repos/microsoft/PowerToys/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/PowerToys/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.WindowsTerminal to Update List
    id = "Microsoft.WindowsTerminal"
    JSON = requests.get("https://api.github.com/repos/microsoft/terminal/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/terminal/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msixbundle")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Microsoft.XMLNotepad to Update List
    id = "Microsoft.XMLNotepad"
    JSON = requests.get("https://api.github.com/repos/microsoft/XmlNotepad/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/microsoft/XmlNotepad/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msixbundle")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add Notepad++.Notepad++ to Update List
    id = "Notepad++.Notepad++"
    JSON = requests.get("https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not("sig" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add FilenCloud.FilenSync to Update List
    id = "FilenCloud.FilenSync"
    Version = requests.get("https://api.github.com/repos/FilenCloudDienste/filen-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [f"https://cdn.filen.io/desktop/release/filen_x64.exe"]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del Urls, Version, id

# Add Cisco.ClamAV to Update List
    id = "Cisco.ClamAV"
    JSON = requests.get("https://api.github.com/repos/Cisco-Talos/clamav/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/Cisco-Talos/clamav/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi") and ("x64" in each["browser_download_url"]) and not("sig" in each["browser_download_url"])]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add JGraph.Draw to Update List
    id = "JGraph.Draw"
    JSON = requests.get("https://api.github.com/repos/jgraph/drawio-desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/jgraph/drawio-desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not(("no" in each["browser_download_url"]) or ("blockmap" in each["browser_download_url"]))]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add dbeaver.dbeaver to Update List
    id = "dbeaver.dbeaver"
    JSON = requests.get("https://api.github.com/repos/dbeaver/dbeaver/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/dbeaver/dbeaver/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add GitHub.cli to Update List
    id = "GitHub.cli"
    JSON = requests.get("https://api.github.com/repos/cli/cli/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/cli/cli/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi") and not("386" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add UniversityOfAmsterdam.praat to Update List
    id = "UniversityOfAmsterdam.praat"
    JSON = requests.get("https://api.github.com/repos/praat/praat/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/praat/praat/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip") and not("xcodeproj" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id

# Add GodotEngine.GodotEngine to Update List
    id = "GodotEngine.GodotEngine"
    JSON = requests.get("https://api.github.com/repos/godotengine/godot/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = re.search(r'\d+(\.\d+)+', requests.get("https://api.github.com/repos/godotengine/godot/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]).group()
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip") and not(("linux" in each["browser_download_url"]) or ("macos" in each["browser_download_url"]) or ("mono" in each["browser_download_url"]) or ("web" in each["browser_download_url"]))]
    if not version_verify(Version, id):
        report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), Version, GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add prefix-dev.pixi to Update List
    id = "prefix-dev.pixi"
    JSON = requests.get("https://api.github.com/repos/prefix-dev/pixi/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/prefix-dev/pixi/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".msi")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add ONLYOFFICE.DesktopEditors to Update List
    id = "ONLYOFFICE.DesktopEditors"
    JSON = requests.get("https://api.github.com/repos/ONLYOFFICE/DesktopEditors/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ONLYOFFICE/DesktopEditors/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith((".msi", ".exe")) and not("xp" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add clsid2.mpc-hc to Update List
    id = "clsid2.mpc-hc"
    JSON = requests.get("https://api.github.com/repos/clsid2/mpc-hc/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/clsid2/mpc-hc/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe") and not(".zip" in each["browser_download_url"])]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add Rizin.Rizin to Update List
    id = "Rizin.Rizin"
    JSON = requests.get("https://api.github.com/repos/rizinorg/rizin/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rizinorg/rizin/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add Rizin.Cutter to Update List
    id = "Rizin.Cutter"
    JSON = requests.get("https://api.github.com/repos/rizinorg/cutter/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/rizinorg/cutter/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".zip")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
# Add TobyAllen.DocTo to Update List
    id = "TobyAllen.DocTo"
    JSON = requests.get("https://api.github.com/repos/tobya/DocTo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/tobya/DocTo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    '''
# Add TheQucsTeam.Qucs-S to Update List
    id = "TheQucsTeam.Qucs-S"
    JSON = requests.get("https://api.github.com/repos/ra3xdh/qucs_s/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/ra3xdh/qucs_s/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].endswith(".exe")]
    if not version_verify(str_pop(Version, 0), id):
         report_existed(id, Version)
    elif do_list(id, Version, "verify"):
        report_existed(id, Version)
    else:
        Commands.append((command(Komac, id, list_to_str(Urls), str_pop(Version, 0), GH_TOKEN), (id, Version, "write")))
    del JSON, Urls, Version, id
    '''
    # Updating
    if not debug:
        for each in Commands:
            if os.system(each[0]) == 0:
                do_list(*each[1])
    
    # Cleanup the merged branch
    os.system(f"{Komac} cleanup --only-merged --all --token {GH_TOKEN}")
    return Commands

if __name__ == "__main__":
    print("Executed Command: ", [each[0] for each in main()])
