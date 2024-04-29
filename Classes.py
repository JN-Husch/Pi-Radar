import pygame

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
    cat = "X0"
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
    sze = 0     #Size 1 - xs, 2 - s, 3 - m, 4 - l, 5 - xl

class HomePosition:
    lat = 0
    lng = 0
    alt = 0

class Options:
    debug = False
    grid = False
    metric = False
    config_ok = False
    mode = 0
    homePos = HomePosition()
    dis_range = 10
    url = ""
    vers = ""
    source = ""

class Button:
    def __init__(self,txt = "EMPTY!", pos = [0,0], sze = [100,50],tag = "UKN", highlight = False):
        self.txt = txt
        self.pos = pos
        self.sze = sze
        self.rect = None
        self.tag = tag
        self.high = highlight
    
    def CheckMousePos(self):
        pygame.mouse.get_pos()

class Text:
    def __init__(self,txt = "", pos = [0,0], sze = [100,50],tag = "UKN",fnt_sze = 0):
        self.txt = txt        
        self.pos = pos
        self.sze = sze
        self.tag = tag
        self.fnt_sze = fnt_sze

class Rectangle:
    def __init__(self, col =[0,0,0], alpha = 255, pos = [0,0], sze = [100,50],tag = "UKN"):
        self.col = col
        self.alpha = alpha
        self.pos = pos
        self.sze = sze
        self.tag = tag