r"""System plugin:: 
    Use `Log()` for log in the log file."""

from datetime import datetime
import os


now = datetime.now()

def Log(text: str):
    with open("Log.txt", "a") as logFile:
        logMessage = f"{now} - {text}"
        logFile.write(logMessage + "\n")
        logFile.close()
        return logMessage
    
def ReadLog():
    with open("Log.txt", "r") as logFile:
        logs = logFile.read()
        logFile.close()
        return logs
    
def ClearLog(pluginName: str):
    os.remove("Log.txt")
    return Log(f"Log Clear by {pluginName}")