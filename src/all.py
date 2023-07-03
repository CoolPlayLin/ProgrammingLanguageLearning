from time import sleep
import requests
import pathlib
import os, sys

def komac(path: str, debug: bool = False):
    Komac = pathlib.Path(path)/"komac.jar"
    if not debug:
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

def version_verify(version: str, id: str) -> bool:
    if len([v for v in requests.get(f"https://winget.vercel.app/api/winget-pkg-versions?pkgid={id}").json()[id] if v == version]) > 0:
        return False
    else:
        return True

def main():
    Commands = []
    debug = bool([each for each in sys.argv if each == "debug"])
    Komac = komac(pathlib.Path(__file__).parents[0], debug)

    # 更新 Node.js Nightly
    id = "OpenJS.NodeJS.Nightly"
    JSONs = requests.get("https://nodejs.org/download/nightly/index.json", verify=False).json()
    for JSON in JSONs:
        URL = f"https://nodejs.org/download/nightly/{ JSON['version'] }"
        Urls = [clean_string(f"{URL}/node-{JSON['version']}-{each}", {"-win": "", "-msi": ".msi"}) for each in JSON["files"] if each.find("msi") != -1]
        if not version_verify(str_pop(JSON['version'], 0), id):
            print(f"{JSON['version']} has already existed, skip publishing")
        else:
            Commands.append(command(Komac, id, list_to_str(Urls),str_pop(JSON['version'], 0), sys.argv[1]))
        del JSON, URL, Urls, id
        print("sleep 5s")
        sleep(5)

    # 更新
    if not debug:
        for each in Commands:
            os.system(each)
    print(Commands)

if __name__ == "__main__":
    main()