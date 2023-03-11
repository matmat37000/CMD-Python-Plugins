import os, json, subprocess, time, sys
import threading as thread
from socket import gethostname

from systemPlugin import *
from colorama import Fore, Back, Style, init

init(autoreset=True)

pluginDictData = {}
pythonPathOfUser = ""

_version_ = "0.1"
_name_ = "Main System"

class main():
    """Main class"""
    def __init__(self):
        self.paths = [".python-command-prompt", ".python-command-prompt\\plugin", ".python-command-prompt\\pluginvar"]
        self.mainPath = f"{os.path.expanduser('~')}\\{self.paths[0]}"
        self.pluginsDict = {}
        self.data = {}
        self.plugins = []
        
    def init(self):
        
        for num, path in enumerate(self.paths):
            path = f"{os.path.expanduser('~')}\\{path}"
            self.paths[num] = path
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                log.Log(f"Folder '{path}' already exist!")
        
        self.plugins = os.listdir(self.paths[1])
        self.pluginsDict.update({"NumFile": len(self.plugins)})
        
        if not os.path.exists(f"{self.paths[0]}\\GLOBALVARIABLE.json"):
            with open(f"{self.mainPath}\\GLOBALVARIABLE.json", "x") as file:
                file.write("{}")
        if not os.path.exists(f"{self.paths[0]}\\pluginList.json"):
            with open(f"{self.mainPath}\\pluginList.json", "x") as file:
                file.write("{}")
        
        
        with open(f"{self.mainPath}\\GLOBALVARIABLE.json", "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            python = data.get("Python", False)
            pythonPathOfUser = data.get("pythonPath", None)
            if python == False:
                with open(f"{self.mainPath}\\GLOBALVARIABLE.json", "w", encoding="utf-8") as jsonFile:
                    pythonPathOfUser = input("Your current 3.11.2 python path or python command: ")
                    jsonFile.write(json.dumps({"Python": True, "PythonPath": f"{pythonPathOfUser} "}, sort_keys=True))
                    raise Exception("Restart App")
        
        with open(f"{self.mainPath}\\pluginList.json", "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            if data.get("NumFile", 0) == len(self.plugins):
                return [log.Log("All files the same!"), data]
           
        for plugin in self.plugins:
            self.pluginsDict.update({plugin.replace(".py", ""): f"{self.mainPath}\\plugin\\{plugin}"})
        
        with open(f"{self.mainPath}\\pluginList.json", "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(self.pluginsDict, sort_keys=True))
            jsonFile.close()

        return "Updated pluginList.json", data
    
class security():
    
    def __init__(self):
        self.fullpath = os.path.abspath('./systemPlugin/crash.py')
    
    def crashHandler(self):
        return
class commandPrompt():
    def __init__(self):
        pass
    
    def prompt(self):
        print(pythonPathOfUser)
        promptCommand = input(f"\n{Fore.LIGHTGREEN_EX}┏━({Fore.BLUE+Style.BRIGHT}{os.getlogin()}@{gethostname()}{Fore.LIGHTGREEN_EX+Style.NORMAL})-[{Fore.WHITE}{str(os.getcwd())}{Fore.LIGHTGREEN_EX}]\n┗━{Fore.BLUE+Style.BRIGHT}${Fore.WHITE+Style.NORMAL} ") #─(kali㉿kali)-[~]
        promptCommand = promptCommand.split()
        
        if promptCommand == []:
            pass
        elif promptCommand[0] in pluginDictData:
            log.Log(f"{promptCommand[0]}-{promptCommand}")
            self.command(promptCommand[0], promptCommand)
        else:
            print(f"{Fore.RED}'{Style.BRIGHT+promptCommand[0]+Style.NORMAL}' is not recognized as an internal or external command or external command, an executable program or a command file.")
        
    def command(self, command, argsList:list=[]):
        exe = ["python", f'{pluginDictData[command]}']
        del argsList[0]
        subprocess.call(exe + argsList)

initDef = main().init()

print(initDef[0])
pluginDictData = initDef[1]
thread.Thread(target=security().crashHandler).start()

fullpath = os.path.abspath('./systemPlugin/crash.py')

while True:
    commandPrompt().prompt()
