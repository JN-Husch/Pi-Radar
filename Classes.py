class Aircraft:
    hex = ""
    flt = ""
    reg = ""
    swk = ""
    lat = -999
    lng = -999
    alt = -999
    spd = -999
    trk = -999
    dis = -999
    ang = -999
    time = 0
    drawn = False

class RadarTarget:
    dis = 0
    ang = 0
    fade = 1000
    trk = 0
    spd = 0
    age = 0
    cls = ""

class HomePosition:
    lat = 0
    lng = 0
    alt = 0