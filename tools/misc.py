
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

def dontwice(fromlist,tolist,maxtries,quart=None,stilladd=False,di=0,qfr=None):
    """" try to add no unit twice to the list
    from the list fromlist, to the list tolist
    will not add it if already present

    if the tolist is a printedlist, use the quart argument to
    indicate positioning clues, else leave it as None

    if the fromlist is a printedlist, use the qfr (quart fr) argument to
    indicate positioning clues, else leave it as None

    if stilladd is true, it will try to add the following element to tolist,
    else, nothing will be done upon failure """
    if quart is not None:
        a1,a2,a3,a4 = quart
        utolist = [x for _,_,_,_,x in tolist]
    else:
        utolist = tolist.copy()
    if qfr is not None:
        a1,a2,a3,a4 = qfr
        ufromlist = [x for _,_,_,_,x in fromlist]
    else:
        ufromlist = fromlist.copy()
    TRIES = di
    tau = ufromlist[TRIES]
    if stilladd:
        while tau in utolist and TRIES - di < maxtries:
            TRIES += 1
            tau = ufromlist[TRIES % len(ufromlist)]

        if TRIES >= maxtries:
            print("max tries")
        else:
            if quart is not None:
                tolist.append((a1,a2,a3,a4,tau))
            else:
                tolist.append(tau)
    else:
        if tau in utolist:
            return
        else:
            if quart is not None:
                tolist.append((a1,a2,a3,a4,tau))
            else:
                tolist.append(tau)


