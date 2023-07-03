from time import sleep
from main import *

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
        del URL, Urls

    # 更新
    if not debug:
        for each in Commands:
            os.system(each)
            print("sleep 5s")
            sleep(5)
    print(Commands)

if __name__ == "__main__":
    main()