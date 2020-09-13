
def purify(L):
    """ supresses multiples instances in the list, so that in the end, each
    element is present at most once.

    The remaining element is the leftmost, and the order is preserved."""
    seen = []
    for a in L:
        if a not in seen:
            seen.append(a)
    return seen