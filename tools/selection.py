
def box(mx,x,Mx,my,y,My):
    return (mx <= x and x <= Mx and my <= y and y <= My)

def szone(mp,w):
    """
    int * int -> world -> zone

    mp : mouse position
    w : world
    returns a z in w
    """
    """
    for c in w.continents:
        for z in c.zones:
            for bx in z.boxes:
                if b(bx[0],bx[1],bx[2],bx[3]):
                    return z
    """
    mpx = mp[0]
    mpy = mp[1]
    def b(mx,Mx,my,My,z=None):
        if z is not None:
            if (mx,Mx,my,My) not in z.boxes:
                z.ab(mx,Mx,my,My)
        return box(mx,mpx,Mx,my,mpy,My)

    if  b(30,334,250,600,w["alaska"]) or  b(331,406,496,666,w["alaska"]):
        return w["alaska"]
    if b(338,1017,250,490,w["nunavut"]):
        return w["nunavut"]
    if b(400,738,500,783,w["alberta"]):
        return w["alberta"]
    if b(742,997,512,782,w["ontario"]):
        return w["ontario"]
    if b(995,1314,486,869,w["quebec"]):
        return w["quebec"]
    if b(1082,1589,36,446,w["groenland"]) or b(1252,1419,446,596,w["groenland"]):
        return w["groenland"]
    if b(431,728,782,1140,w["westernstates"]) or b(728,815,770,995,w["westernstates"]):
        return w["westernstates"]
    if b(496,716,1137,1277,w["centralamerica"]) or b(550,822,1277,1376,w["centralamerica"]) or b(711,800,1376,1531,w["centralamerica"]):
        return w["centralamerica"]
    if b(712,1030,897,1200,w["easternstates"]) or b(1030,1170,880,1070,w["easternstates"]):
        return w["easternstates"] # must be placed behind other states
    if b(790,1268,1445,1655,w["venezuela"]):
        return w["venezuela"]
    if b(766,900,1662,1900,w["peru"]) or b(900,1180,1816,1992,w["peru"]):
        return w["peru"]
    if b(947,1261,2016,2614, w["argentina"]):
        return w["argentina"]
    if b(874,1507,1620,1829, w["brasil"]) or b(1133,1450,1829,2044, w["brasil"]):
        return w["brasil"]
    if b(1639,1990,1421,1925,w["northafrica"]) or b(1990,2191,1641,1888,w["northafrica"]):
        return w["northafrica"]
    if b(2030,2415,2161,2600,w["southafrica"]):
        return w["southafrica"]
    if b(2181,2428,1661,1950, w["eastafrica"]) or b(2300,2489,2040,2189, w["eastafrica"]) or b(2348,2595,1810,2040, w["eastafrica"]):
        return w["eastafrica"]
    if b(1975,2340,1861,2134,w["congo"]):
        return w["congo"]
    if b(2027,2366,1460,1655,w["egypt"]):
        return w["egypt"]
    if b(2505,2605,2307,2517,w["madagascar"]) or b(2587,2643,2230,2374,w["madagascar"]):
        return w["madagascar"]
    if b(1597,1785,1206,1400,w["west"]) or b(1657,1862,1041,1251,w["west"]):
        return w["west"]
    if b(1500,1759,645,986,w["greatbritain"]):
        return w["greatbritain"]
    if b(1601,1819,467,612,w["iceland"]):
        return w["iceland"]
    if b(1823,2161,740,1060,w["north"]):
        return w["north"]
    if b(1877,2183,1072,1382,w["south"]):
        return w["south"]
    if b(1877,2110,327,719,w["scandinavia"]) or b(2093,2215,216,614,w["scandinavia"]):
        return w["scandinavia"]
    if b(2162,2535,321,1203,w["ukraine"]) or b(2489,1696,318,802,w["ukraine"]):
        return w["ukraine"]
    if b(2172,2743,1203,1452,w["middleeastern"]) or b(2366,2748,1431,1758,w["middleeastern"]):
        return w["middleeastern"]
    if b(2489,2882,908,1177, w["afghanistan"]):
        return w["afghanistan"]
    if b(2679,2958,209,861, w['ural']):
        return w['ural']
    if b(2810,3207,63,636,w["siberia"]) or b(2922,3105,618,871,w["siberia"]):
        return w["siberia"]
    if b(3095,3359,493,802,w["tchita"]):
        return w["tchita"]
    if b(3187,3460,144,429,w["yakutia"]):
        return w["yakutia"]
    if b(3667,3822,693,1158,w["japan"]):
        return w["japan"]
    if b(3121,3589,716,1081,w["mongolia"]):
        return w["mongolia"]
    if b(3465,3821,130,882, w["kamschatka"]):
        return w["kamschatka"]
    if b(2912,3504,1038,1418,w["china"]):
        return w["china"]
    if b(2736,3148,1248,1794,w['india']):
        return w['india']
    if b(3148,3418,1378,1774, w["siam"]):
        return w["siam"]
    if b(3104,3488,1812,2152,w["indonesia"]):
        return w['indonesia']
    if b(3498,3841,1755,2016,w["newguinea"]):
        return w["newguinea"]
    if b(3328,3600,2112,2575,w["westaustralia"]) or b(3599,3768,2347,2631,w["westaustralia"]):
        return w["westaustralia"]
    if b(3597,4000,2073,2640,w["eastaustralia"]):
        return w["eastaustralia"]
