import requests
import pathlib
import os, sys

JSON = requests.get("https://nodejs.org/download/nightly/index.json").json()[0]
URL = f"https://nodejs.org/download/nightly/{ JSON['version'] }"
FILEs = [f"{URL}/node-{JSON['version']}-{each.replace('-msi', '.msi')}".replace('-win', '') for each in JSON["files"] if each.find("msi") != -1]
Komac = pathlib.Path(__file__).parents[0]/"komac.jar"

with open(Komac, "wb+") as f:
    file = requests.get("https://gh.api-go.asia/https://github.com/russellbanks/Komac/releases/download/v1.8.0/Komac-1.8.0-all.jar")
    f.write(file.content)
V = list(JSON['version'])
V.pop(0)
V = "".join(V)
COMMAND = "java -jar {} update --urls {} --version {} --submit --token {}".format(Komac,str(FILEs).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""), V, sys.argv[1])
os.system(COMMAND)