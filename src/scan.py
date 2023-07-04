import os
import pathlib
import yaml
import requests
from threading import Thread

class TaskManager:
    __slots__ = ("task", "status", "task_limit", "died_task")

    def __init__(self, task_limit: int = 0, number: int = 1) -> None:
        self.task: dict[str, list[list[Thread], list[Thread]]] = {}
        for i in range(number):
            self.task[str(i)] = [[], []]
        self.task_limit = int(task_limit)
        self.died_task: list[Thread] = []
        self.status = True

    def run(self) -> bool:
        try:
            while self.status:
                if len(self.task['0'][0]) == 0:
                    break
                for id in self.task:
                    self.died_task.extend(
                        [t for t in self.task[id][1] if not t.is_alive()])
                    self.task[id][1] = [
                        t for t in self.task[id][1] if t.is_alive()]
                    for t in self.task[id][0]:
                        if not isinstance(t, Thread):
                            self.task[id][0].remove(t)
                            continue
                        elif self.task_limit:
                            if len(self.task[id][1]) >= self.task_limit:
                                continue
                        self.task[id][1].append(t)
                        t.start()
                        self.task[id][0].remove(t)
        except BaseException as e:
            error = Exception("任务管理器异常退出, 原因：{}".format(e))
            raise error from e
        return True

    def AddTask(self, Task: Thread, id: int) -> bool:
        if isinstance(Task, Thread) and str(id) in self.task:
            self.task[str(id)][0].append(Task)
            return True
        else:
            return False

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

def check(url) -> None:
    print(f"Starting Check: {url}")
    if requests.get(url).status_code >= 401:
        print(f"{url} Scanning Fail\n")
    else:
        print(f"{url} Scanning Pass\n")

def main():
    PATHs = get_manifest_path()[0]
    task = TaskManager(0)
    Files = []
    find_installers(PATHs, Files)
    for m in Files:
        try:
            with open(m, "r", encoding="utf-8") as f:
                Manifest = yaml.load(f.read(), yaml.Loader)
                for url in Manifest["Installers"]:
                    task.AddTask(Thread(target=check, kwargs=dict(url=url["InstallerUrl"])), 0)
        except BaseException:
            continue
    task.run()

if __name__ == "__main__":
    main()