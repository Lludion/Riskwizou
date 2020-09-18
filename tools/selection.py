
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
    if b(742,997,512,782):
        return w["ontario"]
    if b(995,1314,486,869):
        return w["quebec"]
    if b(1082,1589,36,446) or b(1252,1419,446,596):
        return w["groenland"]
    if b(431,728,782,1140) or b(728,815,770,995):
        return w["westernstates"]
    if b(496,716,1137,1277) or b(550,822,1277,1376) or b(711,800,1376,1531):
        return w["centralamerica"]
    if b(712,1030,897,1200) or b(1030,1170,880,1070):
        return w["easternstates"] # must be placed behind other states
    if b(790,1268,1445,1655):
        return w["venezuela"]
    if b(766,900,1662,1900) or b(900,1180,1816,1992):
        return w["peru"]
    if b(947,1261,2016,2614):
        return w["argentina"]
    if b(874,1507,1620,1829) or b(1133,1450,1829,2044):
        return w["brasil"]
    if b(1639,1990,1421,1925) or b(1990,2191,1641,1888):
        return w["northafrica"]
    if b(2030,2415,2161,2600):
        return w["southafrica"]
    if b(2181,2428,1661,1950) or b(2300,2489,2040,2189) or b(2348,2595,1810,2040):
        return w["eastafrica"]
    if b(1975,2340,1861,2134):
        return w["congo"]
    if b(2027,2366,1460,1655):
        return w["egypt"]
    if b(2505,2605,2307,2517) or b(2587,2643,2230,2374):
        return w["madagascar"]
    if b(1597,1785,1206,1400) or b(1657,1862,1041,1251):
        return w["west"]
    if b(1500,1759,645,986):
        return w["greatbritain"]
    if b(1601,1819,467,612):
        return w["iceland"]
    if b(1823,2161,740,1060):
        return w["north"]
    if b(1877,2183,1072,1382):
        return w["south"]
    if b(1877,2110,327,719) or b(2093,2215,216,614):
        return w["scandinavia"]
    if b(2162,2535,321,1203) or b(2489,1696,318,802):
        return w["ukraine"]
    if b(2172,2743,1203,1452) or b(2366,2748,1431,1758):
        return w["middleeastern"]
    if b(2489,2882,908,1177):
        return w["afghanistan"]
    if b(2679,2958,209,861):
        return w['ural']
    if b(2810,3207,63,636) or b(2922,3105,618,871):
        return w["siberia"]
    if b(3095,3359,493,802):
        return w["tchita"]
    if b(3187,3460,144,429):
        return w["yakutia"]
    if b(3667,3822,693,1158):
        return w["japan"]
    if b(3121,3589,716,1081):
        return w["mongolia"]
    if b(3465,3821,130,882):
        return w["kamschatka"]
    if b(2912,3504,1038,1418):
        return w["china"]
    if b(2736,3148,1248,1794):
        return w['india']
    if b(3148,3418,1378,1774):
        return w["siam"]
    if b(3104,3488,1812,2152):
        return w['indonesia']
    if b(3498,3841,1755,2016):
        return w["newguinea"]
    if b(3328,3600,2112,2575) or b(3599,3768,2347,2631):
        return w["westaustralia"]
    if b(3597,4000,2073,2640):
        return w["eastaustralia"]
