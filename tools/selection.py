
def box(mx,x,Mx,my,y,My):
    return (mx <= x and x <= Mx and my <= y and y <= My)

def szone(mp,w):
    """
    int * int -> world -> zone

    mp : mouse position
    w : world
    returns a z in w
    """
    mpx = mp[0]
    mpy = mp[1]
    def b(mx,Mx,my,My):
        return box(mx,mpx,Mx,my,mpy,My)

    if (30 <= mpx and mpx <= 334 and 250 <= mpy and mpy <= 600) or (331 <= mpx and mpx <= 406 and 496 <= mpy and mpy <= 666):
        return w["alaska"]
    if b(338,1017,250,490):
        return w["nunavut"]
    if b(400,738,500,783):
        return w["alberta"]
    if b(742,997,512,782)
        return w["ontario"]
    if b(995,1314,486,869):
        return w["quebec"]
    if b(1082,1589,36,592):
        return w["groenland"]

