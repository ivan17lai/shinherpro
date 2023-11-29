import json
import datetime

global logSaveOn
global title

def on(titleIn):
    global logSaveOn
    global title
    title = titleIn
    logSaveOn = True

def addLog(logFrom,UserNameSave,logIn):
    if logSaveOn:
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = {"title": title, "time": nowTime,"logFrom":logFrom,"UserCode":UserNameSave, "log": logIn}

        with open("log.json", "a", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False)
            f.write('\n')
