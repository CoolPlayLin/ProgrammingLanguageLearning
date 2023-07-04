import os
import pathlib
import yaml
import requests

def find_installers(path: pathlib.Path, files: list) -> None:
    if path.is_file():
        if path.stem.find("installer") != -1:
            files.append(path)
    elif path.is_dir():
        for item in os.listdir(path):
            item_path = path / item
            find_installers(item_path, files)

def get_manifest_path() -> list[pathlib.Path]:
    PATH = []
    PATHs = pathlib.Path(__file__).parents
    for i in PATHs:
        if bool([each for each in os.listdir(i) if each.find("winget-pkgs") != -1]):
            path = i / "winget-pkgs" / "manifests"
            if path.exists():
                PATH.append(path)
        elif bool([each for each in os.listdir(i) if each.find("manifests") != -1]):
            path = i / "manifests"
            if path.exists():
                PATH.append(path)
    return PATH

def main():
    PATHs = get_manifest_path()[0]
    Files = []
    find_installers(PATHs, Files)
    for m in Files:
        with open(m, "r", encoding="utf-8") as f:
            Manifest = yaml.load(f.read(), yaml.Loader)
            for url in Manifest["Installers"]:
                try:
                    if requests.get(url["InstallerUrl"]).status_code > 401:
                        print("Scanning Fail")
                    else:
                        print("Scanning Pass")
                except:
                    continue

if __name__ == "__main__":
    main()