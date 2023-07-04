import os
import pathlib

def find_installers(path: pathlib.Path, files: list) -> None:
    print(len(files))
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
    print(Files)
    return Files

if __name__ == "__main__":
    main()