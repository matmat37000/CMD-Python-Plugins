_version_ = "0.1"
_name_ = "Main System"


import os
import json
from cmd import Cmd

from systemPlugin import *

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
        
        with open("pluginList.json", "r") as jsonFile:
            data = json.load(jsonFile)
            if data["NumFile"] == len(plugins):
                # log.Log("All files the same!")
                return log.Log("All files the same!")
                
        for plugin in plugins:
            self.pluginsDict.update({plugin: f"./plugin/{plugin}"})
            print(plugin)
        
        with open("pluginList.json", "w") as jsonFile:
            jsonFile.write(json.dumps(self.pluginsDict, sort_keys=True))
            jsonFile.close()

    def pluginStart():
        return
    
class security():
    
    def crashHandler():
        return

class commandPrompt(Cmd):
    
    def do_log(self, inp):
        
        argsCount: int = 1
        
        args: list = inp.split()
        if "-r" in args:
            print(log.ReadLog())
        elif "-c" in args:
            log.ClearLog(_name_)
        else:
            print(f"'log' take {argsCount} but 0 was given.")
    
    def do_exit(self, inp):
        print("Bye")
        return True
    

print(main().init())
commandPrompt().cmdloop()