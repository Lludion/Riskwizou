
def defeat(units,survivors=""):
    # units is defeated, some units die
    for u in units:
        if u.pm >= 2 and survivors != "no":
            u.pm -= 1
        else:
            u.dies()
            print(u,"dies","!")