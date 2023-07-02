import requests
import pathlib
import os, sys

def komac(path: str):
    Komac = pathlib.Path(path)/"komac.jar"
    with open(Komac, "wb+") as f:
        file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.8.0/Komac-1.8.0-all.jar", verify=False)
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

def main():
    Commands = []
    Komac = komac(pathlib.Path(__file__).parents[0])

    # 更新 Node.js Nightly
    JSON = requests.get("https://nodejs.org/download/nightly/index.json", verify=False).json()[0]
    URL = f"https://nodejs.org/download/nightly/{ JSON['version'] }"
    Urls = [clean_string(f"{URL}/node-{JSON['version']}-{each}", {"-win": "", "-msi": ".msi"}) for each in JSON["files"] if each.find("msi") != -1]
    Commands.append(command(Komac, "OpenJS.NodeJS.Nightly", list_to_str(Urls),str_pop(JSON['version'], 0), sys.argv[1]))
    del JSON, URL, Urls

    # 更新 Clash for Windows
    JSON = requests.get("https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest", verify=False).json()["assets"]
    Version = requests.get("https://api.github.com/repos/Fndroid/clash_for_windows_pkg/releases/latest", verify=False).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1]
    Commands.append(command(Komac, "Fndroid.ClashForWindows", list_to_str(Urls), Version, sys.argv[1]))
    del JSON, Urls, Version

    # 更新 DooTask
    JSON = requests.get("https://api.github.com/repos/kuaifan/dootask/releases/latest", verify=False).json()["assets"]
    Version = requests.get("https://api.github.com/repos/kuaifan/dootask/releases/latest", verify=False).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and each["browser_download_url"].find("blockmap") == -1]
    Commands.append(command(Komac, "KuaiFan.DooTask", list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version

    # 更新 Listen 1
    JSON = requests.get("https://api.github.com/repos/listen1/listen1_desktop/releases/latest", verify=False).json()["assets"]
    Version = requests.get("https://api.github.com/repos/listen1/listen1_desktop/releases/latest", verify=False).json()["tag_name"]
    Urls = [each["browser_download_url"] for each in JSON if each["browser_download_url"].find("exe") != -1 and (each["browser_download_url"].find("ia32") != -1 or each["browser_download_url"].find("x64") != -1) and each["browser_download_url"].find("blockmap") == -1]
    Commands.append(command(Komac, "listen1.listen1", list_to_str(Urls), str_pop(Version, 0), sys.argv[1]))
    del JSON, Urls, Version

    # 更新
    for each in Commands:
         os.system(each)

if __name__ == "__main__":
    main()