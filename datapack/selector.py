def entity(name:str=None,type:str=None):
    out = ""
    for i in [('name',name),('type',type)]:
        if i[1] is None: continue
        out += f"{i[0]}={i[1]}"
    return "@e" if not out else f"@e[{out}]"

def player(name:str=None):
    out = ""
    for i in [('name',name)]:
        if i[1] is None: continue
        out += f"{i[0]}={i[1]}"
    return "@p" if not out else f"@p[{out}]"

def me():
    return "@s"

def self():
    return "@s"