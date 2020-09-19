
def colorname(dstr,own=None):
    if own is None:
        c1 = c2 = c3 = 165
        ownname = dstr("independent")
    else:
        c1 = own.color[0]
        c2 = own.color[1]
        c3 = own.color[2]
        ownname = dstr(own.name)
    return c1,c2,c3,ownname

def atkwin(dest,chosen):
    if not dest.troops:
        for u in chosen:
            u.move(dest)
    else:
        for u in chosen:
            u.pm -= 1