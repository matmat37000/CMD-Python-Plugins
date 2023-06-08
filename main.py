""""Main File"""
import json
import os
import subprocess
import sys
from socket import gethostname

from colorama import Fore, Style, init
from systemPlugin import log

init(autoreset=True)

pluginDictData = {}
DEFAULTPROMPT = "%V┏━(%B%SB%L@%V%SN)-[%W%DR%V]\n┗━%B%SB$%W%SN "
REPLACEDATA = {
    # Commands
    "%L": f"{os.getlogin()}",
    "%H": f"{gethostname()}",
    # Colors
    "%R": f"{Fore.LIGHTRED_EX}",
    "%M": f"{Fore.LIGHTMAGENTA_EX}",
    "%BL": f"{Fore.LIGHTBLACK_EX}",
    "%Y": f"{Fore.LIGHTYELLOW_EX}",
    "%B": f"{Fore.LIGHTBLUE_EX}",
    "%C": f"{Fore.LIGHTCYAN_EX}",
    "%V": f"{Fore.LIGHTGREEN_EX}",
    "%W": f"{Fore.LIGHTWHITE_EX}",
    "%SB": f"{Style.BRIGHT}",
    "%SN": f"{Style.NORMAL}"
}

_version_ = "0.1"
_name_ = "Main System"

__TITLE1__ = """
  _______                      _  _____         _    _                   
 |__   __|                    (_)|  __ \\       | |  | |                  
    | |  ___  _ __  _ __ ___   _ | |__) |_   _ | |_ | |__    ___   _ __  
    | | / _ \\| '__|| '_ ` _ \\ | ||  ___/| | | || __|| '_ \\  / _ \\ | '_ \\ 
    | ||  __/| |   | | | | | || || |    | |_| || |_ | | | || (_) || | | |
    |_| \\___||_|   |_| |_| |_||_||_|     \\__, | \\__||_| |_| \\___/ |_| |_|
                                          __/ |                          
                                         |___/   V.0.1 | By Mathiol """

class Main():
    """Main class"""
    def __init__(self):
        self.paths = [".python-command-prompt", ".python-command-prompt\\plugin", ".python-command-prompt\\pluginvar"]
        self.main_path = f"{os.path.expanduser('~')}\\{self.paths[0]}"
        self.plugin_dict = {}
        self.data = {}
        self.plugins = []
        self.prompt: str = ""
        self.python_path_of_user: str = ""
        
    def init(self):
        """"Init the command prompt"""
        for num, path in enumerate(self.paths):
            path = f"{os.path.expanduser('~')}\\{path}"
            self.paths[num] = path
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                log.Log(f"Folder '{path}' already exist!")
        
        self.plugins = os.listdir(self.paths[1])
        self.plugin_dict.update({"NumFile": len(self.plugins)})
        
        # Create settings json file
        if not os.path.exists(f"{self.paths[0]}\\settings.json"):
            with open(f"{self.main_path}\\settings.json", "x", encoding='utf-8') as file:
                file.write("{}")
        # Create plugin list json file
        if not os.path.exists(f"{self.paths[0]}\\pluginList.json"):
            with open(f"{self.main_path}\\pluginList.json", "x", encoding='utf-8') as file:
                file.write("{}")
        
        # Read settings.json and load settings into python_path_of_user and self.prompt
        with open(f"{self.main_path}\\settings.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            python = data.get("Python", False)
            self.python_path_of_user = data.get("PythonPath", None)
            self.prompt = data.get("Prompt", None)
            
            if python is False:
                with open(f"{self.main_path}\\settings.json", "w", encoding="utf-8") as json_file:
                    self.python_path_of_user = input("Your current 3.11.2 python path or python command: ")
                    json_file.write(json.dumps({"Python": True, "PythonPath": python_path_of_user, "Prompt": DEFAULTPROMPT}, sort_keys=True, indent=3))
                    input("Restart App")
                    return
            elif self.prompt is None:
                with open(f"{self.main_path}\\settings.json", "w", encoding="utf-8") as json_file:
                    json_file.write(json.dumps({"Python": True, "PythonPath": python_path_of_user, "Prompt": DEFAULTPROMPT}, sort_keys=True, indent=3))
                self.prompt = DEFAULTPROMPT

            for replaced, replace in REPLACEDATA.items():
                self.prompt = self.prompt.replace(replaced, replace)
            
        # Update list of plugin
        with open(f"{self.main_path}\\pluginList.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            if data.get("NumFile", 0) == len(self.plugins):
                return log.Log("All files the same!"), data, python_path_of_user, self.prompt

        for plugin in self.plugins:
            self.plugin_dict.update({
                plugin.replace(".py", ""): f"{self.main_path}\\plugin\\{plugin}"})
        with open(f"{self.main_path}\\pluginList.json", "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(self.plugin_dict, sort_keys=True, indent=3))
            json_file.close()
        # for name, replace in enumerate(replaceData):
        #     self.prompt = self.prompt.replace(name, replace)

        return ("Updated pluginList.json", data, python_path_of_user, self.prompt)
    
class Security():
    """Unused Security program"""
    def __init__(self):
        self.fullpath = os.path.abspath('./systemPlugin/crash.py')

class CommandPrompt():
    """Execution of commands class"""
    def __init__(self):
        pass
    
    def prompt(self):
        """Prompt"""
        prompt_command = input(f"\n{prompt}".replace("%DR", f"{os.getcwd()}")) # {Fore.LIGHTGREEN_EX}┏━({Fore.BLUE+Style.BRIGHT}{os.getlogin()}@{gethostname()}{Fore.LIGHTGREEN_EX+Style.NORMAL})-[{Fore.WHITE}{str(os.getcwd())}{Fore.LIGHTGREEN_EX}]\n┗━{Fore.BLUE+Style.BRIGHT}${Fore.WHITE+Style.NORMAL} ") #─(kali㉿kali)-[~]
        prompt_command = prompt_command.split()
        
        if prompt_command == [] or prompt_command == "":
            pass
        elif prompt_command[0] in pluginDictData:
            log.Log(f"{prompt_command[0]}-{prompt_command}")
            self.command(prompt_command[0], prompt_command)
        elif prompt_command[0] == "cd":
            os.chdir(prompt_command[1])
        elif prompt_command[0] == "exit":
            sys.exit(0)
        else:
            command = prompt_command[0]
            try:
                del prompt_command[0]
                subprocess.run([command] + prompt_command, shell=True, check=False)
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}'{Style.BRIGHT+command+Style.NORMAL}' is not recognized as an internal or external command or external command, an executable program or a command file.")
        
    def command(self, command, args_list:list):
        """Execution part"""
        exe = [python_path_of_user, f'{pluginDictData[command]}']
        del args_list[0]
        subprocess.call(exe + args_list)

initDef = Main().init()
pluginDictData = initDef[1]
python_path_of_user = initDef[2]
prompt = initDef[3]
# thread.Thread(target=Security().crashHandler).start()

fullpath = os.path.abspath('./systemPlugin/crash.py')

os.system('cls')
print(Style.BRIGHT+Fore.YELLOW+__TITLE1__)
while True:
    try:
        CommandPrompt().prompt()
    except KeyboardInterrupt:
        print("")