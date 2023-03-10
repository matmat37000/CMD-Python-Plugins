_version_ = "0.1"
_name_ = "Main System"

import os, json, subprocess, time, sys
import threading as thread
from socket import gethostname

from systemPlugin import *
from colorama import Fore, Back, Style, init

init(autoreset=True)

pluginDictData = {}

class main():
    """Main class"""
    def __init__(self):
        self.paths = ["./plugin", "./pluginvar"]
        self.pluginsDict = {}
        self.data = {}
        
    def init(self):
        
        for path in self.paths:
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                log.Log(f"Folder '{path}' already exist!")
        
        plugins = os.listdir(self.paths[0])
        self.pluginsDict.update({"NumFile": len(plugins)})
        
        with open("pluginList.json", "r", encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            if data["NumFile"] == len(plugins):
                # log.Log("All files the same!")
                return [log.Log("All files the same!"), data]
                
        for plugin in plugins:
            self.pluginsDict.update({plugin.replace(".py", ""): os.path.abspath(f"./plugin/{plugin}")})
            print(os.path.abspath(f"./{plugin}"))
        
        with open("pluginList.json", "w", encoding="utf-8") as jsonFile:
            jsonFile.write(json.dumps(self.pluginsDict, sort_keys=True))
            jsonFile.close()
        return "Updated pluginList.json", data
    
class security():
    
    def __init__(self):
        self.fullpath = os.path.abspath('./systemPlugin/crash.py')
    
    def crashHandler(self):
        # while True:
        #     try:
        #         commandPrompt().prompt()
        #     except Exception as err:
        #         subprocess.Popen(f"python \"{self.fullpath}\" {err}")
        return

# Old CMD sytem with module 'cmd' | Note: to use this class, add oldCommandPrompt().cmdloop() at the end of this code and in oldCommandPrompt() add 'Cmd' between the bracket
class oldCommandPrompt():
    
    def do_log(self, inp):
        '''get log plugin commands.
        -r: read and print the log.
        -c: clear the log file.'''
        
        argsCount: int = 1
        args: list = inp.split()
        
        if len(args)!=argsCount:
            print(Fore.RED+"*** invalid number of arguments")
            return
        
        if "-r" in args:
            print(log.ReadLog())
        elif "-c" in args:
            log.ClearLog(_name_)
        else:
            print(Fore.RED+f"***'log' take {argsCount} but 0 was given.")
    
    def complete_log(self, text, line, begidx, endidx):
        _AVAILABLE_LOG_ARGS = ('-r', '-c')
        return [i for i in _AVAILABLE_LOG_ARGS if i.startswith(text)]
    
    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True
    
    def do_cls(self, inp):
        os.system('cls')

class commandPrompt():
    def __init__(self):
        pass
    
    def prompt(self):
        promptCommand = input(f"┏━{os.getlogin()}@{gethostname()}\n┗━{str(os.getcwd())}$ ")
        log.Log(promptCommand)
        # log.Log(str(pluginDictData))
        promptCommand = promptCommand.split()
        
        
        if promptCommand[0] in pluginDictData:
            self.command(promptCommand[0], promptCommand)
        
        
    def command(self, command, argsList:list=[]):
        exe = [sys.executable, f'{pluginDictData[command]}']
        del argsList[0]
        subprocess.call(exe + argsList)

initDef = main().init()

print(initDef[0])
pluginDictData = initDef[1]
thread.Thread(target=security().crashHandler).start()

fullpath = os.path.abspath('./systemPlugin/crash.py')

while True:
    commandPrompt().prompt()
    # try:
    # except Exception as err:
    #     subprocess.call(f'start python \"{fullpath}\"', shell=True)
