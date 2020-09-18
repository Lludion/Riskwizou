
def purify(L):
    """ supresses multiples instances in the list, so that in the end, each
    element is present at most once.

    The remaining element is the leftmost, and the order is preserved."""
    seen = []
    for a in L:
        if a not in seen:
            seen.append(a)
    return seen

def forall(f,L):
    """returns True iff f(L[i]) for all i"""
    v = True
    for e in L:
        v &= f(e)
    return v

def fullpm(u,z):
    return [x for x in z.troops if x.name == u().name and x.pm == x.pmmax]