import requests
import pathlib
import os, sys

def komac(path: str):
    Komac = pathlib.Path(path)/"komac.jar"
    with open(Komac, "wb+") as f:
        file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.8.0/Komac-1.8.0-all.jar")
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

def main():
    Commands = []
    Komac = komac(pathlib.Path(__file__).parents[0])
    # 升级Node.js Nightly
    JSON = requests.get("https://nodejs.org/download/nightly/index.json").json()[0]
    URL = f"https://nodejs.org/download/nightly/{ JSON['version'] }"
    Urls = [clean_string(f"{URL}/node-{JSON['version']}-{each}", {"-win": "", "-msi": ".msi"}) for each in JSON["files"] if each.find("msi") != -1]
    Commands.append(command(Komac, "OpenJS.NodeJS.Nightly", Urls,str_pop(JSON['version'], 0), sys.argv[1]))

    # 更新
    for each in Commands:
         os.system(each)

if __name__ == "__main__":
    main()