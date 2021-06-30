import os
import json

def tick(func):
    def wrapper(*args):
        args[0]._tick.append("_last")
        return func(*args)
    return wrapper

def load(func):
    def wrapper(*args):
        args[0]._load.append("_last")
        return func(*args)
    return wrapper

def _check_then_write(path,write):
    if not os.path.exists(path):
        open(path,"x")
    with open(path,"w+") as f:
        f.write(write)

class Execute():
    def __init__(self,parent):
        self.subcommands = []
        parent.commands.append(self)

    def __str__(self):
        return f"execute {' '.join(self.subcommands)}"

    def ex_as(self,target:str):
        self.subcommands.append(f"as {target}")

    def ex_run(self,command):
        self.subcommands.append(f"run {command}")

class Scoreboard():
    def __init__(self,function,objective,add=False,criteria="dummy",displayname=None):
        self.objective = objective
        self.commands = function.commands
        self.displayname = displayname if displayname else objective
        self.trigger = criteria == "trigger"
        if add:
            self.commands.append(f"scoreboard objectives add {objective} {criteria}{(' ' + displayname) if displayname else ''}")

    def delete(self,ret=False):
        if ret:
            return f"scoreboard objectives remove {self.objective}"
        self.commands.append(f"scoreboard objectives remove {self.objective}")

    def setdisplay(self,slot,ret=False):
        if ret:
            return f"scoreboard setdisplay {slot} {self.objective}"
        self.commands.append(f"scoreboard setdisplay {slot} {self.objective}")

    def modify_displayname(self,displayname=None,ret=False):
        if not displayname: displayname = self.objective
        if ret:
            return f"scoreboard objectives modify {self.objective} displayname {json.dumps(displayname,separators=(',', ':'))}"
        self.commands.append(f"scoreboard objectives modify {self.objective} displayname {json.dumps(displayname,separators=(',', ':'))}")

    def modify_rendertype(self,hearts,ret=False):
        if isinstance(hearts,(bool,int)):
            rendertype = "hearts" if hearts else "integer"
        elif isinstance(hearts,str):
            rendertype = "hearts" if hearts.lower() == "hearts" else "integer"
        if ret:
            return f"scoreboard objectives modify {self.objective} rendertype {rendertype}"
        self.commands.append(f"scoreboard objectives modify {self.objective} rendertype {rendertype}")

class Function():
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        self.pack = parent.name
        self.commands = []

    def _save(self):
        fn = os.path.join(self.pack,"data",self.pack.lower(),"functions",f"{self.name}.mcfunction")
        self.commands = [str(command) for command in self.commands]
        _check_then_write(fn,"\n".join(self.commands))

    def say(self,message:str,ret=False):
        if ret:
            return f"say {message}"
        self.commands.append(f"say {message}")

    def kill(self,target:str,ret=False):
        if ret:
            return f"kill {target}"
        self.commands.append(f"kill {target}")

    def teleport(self,target0:str,target1:str,ret=False):
        if ret:
            return f"tp {target0} {target1}"
        self.commands.append(f"tp {target0} {target1}")

    def function(self,function,ret=False):
        if callable(function):
            function = [i for i in dir(self.parent) if getattr(self.parent,i,None) == function][0]
        if ':' not in function:
            function = f"{self.pack.lower()}:{function}"
        if ret:
            return f"function {function}"
        self.commands.append(f"function {function}")

    def execute(self):
        return Execute(self)

    def scoreboard(self,objective,add=False,criteria="dummy",displayname=None):
        return Scoreboard(self,objective,add,criteria,displayname)

    def scoreboard_list(self,ret=False):
        if ret:
            return f"scoreboard objectives list"
        self.commands.append(f"scoreboard objectives list")

    def scoreboard_setdisplay(self,slot,ret=False):
        if ret:
            return f"scoreboard objectives setdisplay {slot}"
        self.commands.append(f"scoreboard objectives setdisplay {slot}")

class Datapack():
    def __init__(self):
        self.name = type(self).__name__
        self.description = getattr(self,"__doc__","A Datapack")
        os.makedirs(os.path.join(self.name,"data",self.name.lower(),"functions"),exist_ok=True)
        fn = os.path.join(self.name,"pack.mcmeta")
        _check_then_write(fn,json.dumps({"pack":{"pack_format":7,"description":self.description}},indent=4))
        self._load = []
        self._tick = []
        for i in dir(self):
            if (i.startswith("_") or i in ["add"]) or not callable(getattr(self,i)): continue
            self.command = Function(i,self)
            getattr(self,i)()
            if self._tick:
                if self._tick[-1] == "_last":
                    self._tick[-1] = f"{self.name.lower()}:{i}"
            if self._load:
                if self._load[-1] == "_last":
                   self._load[-1] = f"{self.name.lower()}:{i}"
            self.command._save()
        if self._load or self._tick:
            os.makedirs(os.path.join(self.name,"data","minecraft","tags","functions"),exist_ok=True)
            if self._tick:
                fn = os.path.join(self.name,"data","minecraft","tags","functions","tick.json")
                _check_then_write(fn,json.dumps({"values":self._tick}))
            if self._load:
                fn = os.path.join(self.name,"data","minecraft","tags","functions","load.json")
                _check_then_write(fn,json.dumps({"values":self._load}))
