import os, json, subprocess, time, sys
import threading as thread
from socket import gethostname

from systemPlugin import *
from colorama import Fore, Back, Style, init

init(autoreset=True)

pluginDictData = {}
pythonPathOfUser = ""
defaultPrompt = "%V┏━(%B%SB%L@%H%V%SN)-[%W%DR%V]\n┗━%B%SB$%W%SN "
prompt = ""
replaceData = {
    # Commands
    "%L": f"{os.getlogin()}",
    "%H": f"{gethostname()}",
    # Colors
    "%R": f"{Fore.LIGHTRED_EX}",
    "%M": f"{Fore.LIGHTMAGENTA_EX}",
    "%B": f"{Fore.LIGHTBLACK_EX}",
    "%Y": f"{Fore.LIGHTYELLOW_EX}",
    "%B": f"{Fore.LIGHTBLUE_EX}",
    "%C": f"{Fore.LIGHTCYAN_EX}",
    "%V": f"{Fore.LIGHTGREEN_EX}",
    "%W": f"{Fore.LIGHTWHITE_EX}",
    "%SB": f"{Style.BRIGHT}",
    "%SN": f"{Style.NORMAL}",
}

_version_ = "0.1"
_name_ = "Main System"

_title1_ = """
  _______                      _  _____         _    _                   
 |__   __|                    (_)|  __ \\       | |  | |                  
    | |  ___  _ __  _ __ ___   _ | |__) |_   _ | |_ | |__    ___   _ __  
    | | / _ \\| '__|| '_ ` _ \\ | ||  ___/| | | || __|| '_ \\  / _ \\ | '_ \\ 
    | ||  __/| |   | | | | | || || |    | |_| || |_ | | | || (_) || | | |
    |_| \\___||_|   |_| |_| |_||_||_|     \\__, | \\__||_| |_| \\___/ |_| |_|
                                          __/ |                          
                                         |___/   V.0.1 | By Mathiol """

class main():
    """Main class"""
    def __init__(self):
        self.paths = [".python-command-prompt", ".python-command-prompt\\plugin", ".python-command-prompt\\pluginvar"]
        self.mainPath = f"{os.path.expanduser('~')}\\{self.paths[0]}"
        self.pluginsDict = {}
        self.data = {}
        self.plugins = []
        self.prompt: str = ""
        
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
        
        # Create settings json file
        if not os.path.exists(f"{self.paths[0]}\\settings.json"):
            with open(f"{self.mainPath}\\settings.json", "x") as file:
                file.write("{}")
        # Create plugin list json file
        if not os.path.exists(f"{self.paths[0]}\\pluginList.json"):
            with open(f"{self.mainPath}\\pluginList.json", "x") as file:
                file.write("{}")
        
        # Read settings.json and load settings into pythonPathOfUser and self.prompt
        with open(f"{self.mainPath}\\settings.json", "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            python = data.get("Python", False)
            pythonPathOfUser = data.get("PythonPath", None)
            self.prompt = data.get("Prompt", None)
            
            if python == False:
                with open(f"{self.mainPath}\\settings.json", "w", encoding="utf-8") as jsonFile:
                    pythonPathOfUser = input("Your current 3.11.2 python path or python command: ")
                    jsonFile.write(json.dumps({"Python": True, "PythonPath": pythonPathOfUser, "Prompt": defaultPrompt}, sort_keys=True, indent=3))
                    input("Restart App")
                    raise
            elif self.prompt == None:
                with open(f"{self.mainPath}\\settings.json", "w", encoding="utf-8") as jsonFile:
                    jsonFile.write(json.dumps({"Python": True, "PythonPath": pythonPathOfUser, "Prompt": defaultPrompt}, sort_keys=True, indent=3))
                self.prompt = defaultPrompt

            for replaced, replace in replaceData.items():
                self.prompt = self.prompt.replace(replaced, replace)
            
        # Update list of plugin
        with open(f"{self.mainPath}\\pluginList.json", "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            if data.get("NumFile", 0) == len(self.plugins):
                return log.Log("All files the same!"), data, pythonPathOfUser, self.prompt
        
        for plugin in self.plugins:
            self.pluginsDict.update({plugin.replace(".py", ""): f"{self.mainPath}\\plugin\\{plugin}"})
        
        with open(f"{self.mainPath}\\pluginList.json", "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(self.pluginsDict, sort_keys=True, indent=3))
            jsonFile.close()
            
        # for name, replace in enumerate(replaceData):
        #     self.prompt = self.prompt.replace(name, replace)

        return ("Updated pluginList.json", data, pythonPathOfUser, self.prompt)
    
class security():
    
    def __init__(self):
        self.fullpath = os.path.abspath('./systemPlugin/crash.py')
    
    def crashHandler(self):
        
        return
class commandPrompt():
    def __init__(self):
        pass
    
    def prompt(self):
        promptCommand = input(f"\n{prompt}".replace("%DR", f"{os.getcwd()}")) # {Fore.LIGHTGREEN_EX}┏━({Fore.BLUE+Style.BRIGHT}{os.getlogin()}@{gethostname()}{Fore.LIGHTGREEN_EX+Style.NORMAL})-[{Fore.WHITE}{str(os.getcwd())}{Fore.LIGHTGREEN_EX}]\n┗━{Fore.BLUE+Style.BRIGHT}${Fore.WHITE+Style.NORMAL} ") #─(kali㉿kali)-[~]
        promptCommand = promptCommand.split()
        
        if promptCommand == [] or promptCommand == "":
            pass
        elif promptCommand[0] in pluginDictData:
            log.Log(f"{promptCommand[0]}-{promptCommand}")
            self.command(promptCommand[0], promptCommand)
        elif promptCommand[0] == "cd":
            os.chdir(promptCommand[1])
        elif promptCommand[0] == "exit":
            sys.exit(0)
        else: 
            command = promptCommand[0]
            try:
                del promptCommand[0]
                subprocess.run([command] + promptCommand, shell=True)
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}'{Style.BRIGHT+command+Style.NORMAL}' is not recognized as an internal or external command or external command, an executable program or a command file.")
        
    def command(self, command, argsList:list=[]):
        exe = [pythonPathOfUser, f'{pluginDictData[command]}']
        del argsList[0]
        subprocess.call(exe + argsList)

initDef = main().init()
pluginDictData = initDef[1]
pythonPathOfUser = initDef[2]
prompt = initDef[3]
thread.Thread(target=security().crashHandler).start()

fullpath = os.path.abspath('./systemPlugin/crash.py')

os.system('cls')
print(Style.BRIGHT+Fore.YELLOW+_title1_)
while True:
    try:
        commandPrompt().prompt()
    except KeyboardInterrupt:
        print("")