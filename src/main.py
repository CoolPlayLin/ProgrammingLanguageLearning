import requests
import pathlib
import os, sys

def komac(path: str, debug: bool = False):
    Komac = pathlib.Path(path)/"komac.jar"
    if not debug:
        with open(Komac, "wb+") as f:
            file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.8.1/Komac-1.8.1-all.jar", verify=False)
            f.write(file.content)
    return Komac

def command(komac: str, id: str, urls: str, version: str, token: str) -> str:
    Commands = "java -jar {} update --id {} --urls {} --version {} --submit --token {}".format(komac, id, urls, version, token)
    return Commands

def clean_string(string: str, keywords: dict[str, str]) -> str:
    for k in keywords:
        string = string.replace(k, keywords[k])
    return string

def str_pop(string: str, index: int)-> str:
        i = list(string)
        i.pop(index)
        i = "".join(i)

        return i

def list_to_str(List: list):
    new = str(List)
    new = clean_string(new, {
         "[": "",
         "]": "",
         " ": "",
         "'": ""
    })
    return new

def version_verify(version: str, id: str) -> bool:
    if len([v for v in requests.get(f"https://winget.vercel.app/api/winget-pkg-versions?pkgid={id}").json()[id] if v == version]) > 0:
        return False
    else:
        return True

def main():
    Commands = []
    debug = bool([each for each in sys.argv if each == "debug"])
    Komac = komac(pathlib.Path(__file__).parents[0], debug)
    Headers = [{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }, {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Authorization": f"Bearer {sys.argv[1]}"
    }]

    # 更新 Node.js Nightly
    id = "OpenJS.NodeJS.Nightly"
    JSON = requests.get("https://nodejs.org/download/nightly/index.json", verify=False, headers=Headers[0]).json()[0]
    URL = f"https://nodejs.org/download/nightly/{ JSON['version'] }"
    Urls = [clean_string(f"{URL}/node-{JSON['version']}-{each}", {"-win": "", "-msi": ".msi"}) for each in JSON["files"] if each.find("msi") != -1]
    if not version_verify(str_pop(JSON['version'], 0), id):
         print(f"{JSON['version']} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls),str_pop(JSON['version'], 0), sys.argv[1]))
    del JSON, URL, Urls, id

    # 更新 Clash for Windows
    id = "Fndroid.ClashForWindows"
    JSON = requests.get("https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1]
    if not version_verify(Version, id):
         print(f"{Version} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls), Version, sys.argv[1]))
    del JSON, Urls, Version, id

    # 更新 DooTask
    id = "KuaiFan.DooTask"
    JSON = requests.get("https://api.github.com/repos/kuaifan/dootask/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kuaifan/dootask/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and each["browser_download_url"].find("blockmap") == -1]
    if not version_verify(str_pop(Version, 0), id):
         print(f"{Version} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version, id

    # 更新 Listen 1
    id = "listen1.listen1"
    JSON = requests.get("https://api.github.com/repos/listen1/listen1_desktop/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/listen1/listen1_desktop/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and (each["browser_download_url"].find("ia32") != -1 or each["browser_download_url"].find("x64") != -1 or each["browser_download_url"].find("arm64") != -1) and each["browser_download_url"].find("blockmap") == -1]
    if not version_verify(str_pop(Version, 0), id):
         print(f"{Version} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version, id

    # 更新 PicGo
    id = "PicGo.PicGo"
    JSON = requests.get("https://api.github.com/repos/Molunerfinn/PicGo/releases/latest", verify=False, headers=Headers[1]).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Molunerfinn/PicGo/releases/latest", verify=False, headers=Headers[1]).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and each["browser_download_url"].find("blockmap") == -1]
    if not version_verify(str_pop(Version, 0), id):
         print(f"{Version} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version, id

    # 更新 PicGo Beta
    id = "PicGo.PicGo.Beta"
    JSON = requests.get("https://api.github.com/repos/Molunerfinn/PicGo/releases", verify=False, headers=Headers[1]).json()[0]["assets"]
    Version = requests.get("https://api.github.com/repos/Molunerfinn/PicGo/releases", verify=False, headers=Headers[1]).json()[0]["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and each["browser_download_url"].find("blockmap") == -1]
    if not version_verify(str_pop(Version, 0), id):
         print(f"{Version} has already existed, skip publishing")
    else:
        Commands.append(command(Komac, id, list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version, id

    # 更新
    if not debug:
        for each in Commands:
            os.system(each)
    print(Commands)

if __name__ == "__main__":
    main()
