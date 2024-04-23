import pygame
from pygame import gfxdraw
import Classes
import math

opt = [False,False,False]

fonts = []

def Draw(mode,screen,raw_tgts,rdr_tgts,dis_range,sweep_angle,fonts_in,opts):
    global opt
    global fonts

    fonts = fonts_in
    opt = opts
    
    col_back = [37,37,37]
    screen.fill(col_back)
    #Draw Grid Lines
    grid_space = 100
    if opts[1]:
        for i in range (-7,7):
            pygame.draw.line(screen,color=[50,50,50],start_pos=[0,screen.get_height() / 2 + grid_space * i + 1],end_pos=[screen.get_width(),screen.get_height() / 2 + grid_space * i + 1],width=1)
            pygame.draw.line(screen,color=[50,50,50],start_pos=[screen.get_width() / 2 + grid_space * i + 1,0],end_pos=[screen.get_width() / 2 + grid_space * i + 1,screen.get_height()],width=1)

    if raw_tgts is not None:
        for tgt in raw_tgts:
            if tgt.dis < dis_range * 5:
                if not tgt.drawn and sweep_angle > tgt.ang and sweep_angle <= tgt.ang + 0.9:
                    rdr_tgt = Classes.RadarTarget()
                    rdr_tgt.pos_x = screen.get_width() / 2 + math.sin(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range
                    rdr_tgt.pos_y = screen.get_height() / 2 - math.cos(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range
                    rdr_tgt.trk = tgt.trk
                    rdr_tgt.ang = tgt.ang
                    rdr_tgt.spd = tgt.spd
                    rdr_tgt.age = tgt.time
                    rdr_tgt.cls = tgt.flt
                    rdr_tgts.append(rdr_tgt)
                    raw_tgts.remove(tgt)

    if mode == 1:
        AnalogDraw(screen,rdr_tgts,dis_range,sweep_angle)
    elif mode == 2:
        DigitalDraw(screen,rdr_tgts,dis_range,sweep_angle)


def AnalogDraw(screen,rdr_tgts,dis_range,sweep_angle):
    global fonts
    col_mark = [205,205,205]
    
    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:
        if rdr_tgt.age < 10:
            col = [round(20 * rdr_tgt.fade / 1000,0) + 37, round(190 * rdr_tgt.fade / 1000,0) + 37, round(20 * rdr_tgt.fade / 1000,0) + 37]
            pygame.draw.circle(screen,color=col,center=[rdr_tgt.pos_x, rdr_tgt.pos_y], radius=7)
        
        rdr_tgt.fade = rdr_tgt.fade * 0.998
        if rdr_tgt.fade < 10:
            rdr_tgts.remove(rdr_tgt)

    #Draw Scan Bar
    for i in range (0,20):
        j = 20 - i
        line_x = screen.get_width() / 2 + math.sin((sweep_angle - j / 5) * math.pi / 180) * 540
        line_y = screen.get_height() / 2 - math.cos((sweep_angle - j / 5) * math.pi / 180) * 540
        col_scan = [39 + 11 * i / 20, 39 + 211 * i / 20, 39 + 11 * i / 20]
        pygame.draw.line(screen,color=col_scan,start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=3)

    DrawMarkings(screen,fonts,col_mark,dis_range)
    
    #Draw Center Circle
    pygame.draw.circle(screen,color=col_mark,center=[screen.get_width() / 2, screen.get_height() / 2], radius=3)


def DigitalDraw(screen,rdr_tgts,dis_range,sweep_angle):
    global fonts
    col_mark = [205,205,205]
    
    DrawMarkings(screen,fonts,col_mark,dis_range)
    
    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:  
        #Draw new targets behind sweep bar      
        if rdr_tgt.age < 10:
            col = [255, 255, 255]
            pygame.draw.circle(screen,color=col,center=[rdr_tgt.pos_x, rdr_tgt.pos_y], radius=3)
            
            if rdr_tgt.spd > 0:
                line_x = rdr_tgt.pos_x + math.sin(rdr_tgt.trk * math.pi / 180) *  rdr_tgt.spd * 100 / dis_range / 60 / 3
                line_y = rdr_tgt.pos_y - math.cos(rdr_tgt.trk * math.pi / 180) *  rdr_tgt.spd * 100 / dis_range / 60 / 3
                pygame.draw.line(screen,col,[rdr_tgt.pos_x, rdr_tgt.pos_y],[line_x, line_y], True)
                img = fonts[1].render(rdr_tgt.cls, True, [175,175,175])
                label_offset_y = -20
                if rdr_tgt.trk >= 270 or rdr_tgt.trk <= 90:
                    label_offset_y = 10
                screen.blit(img, (rdr_tgt.pos_x - 20, rdr_tgt.pos_y + label_offset_y))

        #Remove old targets ahead of sweep bar
        if sweep_angle > rdr_tgt.ang - 1 and sweep_angle < rdr_tgt.ang:
            rdr_tgts.remove(rdr_tgt) 

    #Draw Scan Bar
    line_x = screen.get_width() / 2 + math.sin(sweep_angle * math.pi / 180) * 500
    line_y = screen.get_height() / 2 - math.cos(sweep_angle * math.pi / 180) * 500
    pygame.draw.line(screen,color=[50, 205, 50],start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=2)


def DrawMarkings(screen,fonts,col_mark,dis_range):
    global opt
    
    #Draw range circles
    for i in range(1,6):
        gfxdraw.aacircle(screen,int(screen.get_width() / 2), int(screen.get_height() / 2), 100 * i,col_mark)

        range_unit = "NM"

        if opt[2]:
            range_unit ="KM"

        img = fonts[0].render(str(i * dis_range) + range_unit, True, col_mark)
        screen.blit(img, (screen.get_width() / 2 - 20, screen.get_height() / 2 + 100 * i + 10))
    
    #Draw Indexes
    for i in range(0,16):
        angle = i * 22.5
        len = 0
        
        if angle == 0 or angle == 90 or angle == 270:
            len  = 20
        elif angle == 45 or angle == 135 or angle == 225 or angle == 315:
            len = 15
        else:
            for j in range (1,17):
                if angle == 22.5*j:
                    len = 5
                    continue

        if len > 0:
            line_pos1_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (screen.get_width() / 2 - 39)
            line_pos1_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (screen.get_height() / 2 - 39)
            line_pos2_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (screen.get_width() / 2 - 39 + len)
            line_pos2_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (screen.get_height() / 2 - 39 + len)
            pygame.draw.line(screen,color=col_mark,start_pos=[line_pos1_x, line_pos1_y],end_pos=[line_pos2_x, line_pos2_y], width=2)
    
    for i in range (0,4):
        angle = i * 90
        line_pos1_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (5) 
        line_pos1_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (5)
        line_pos2_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (10)
        line_pos2_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (10)
        pygame.draw.line(screen,color=col_mark,start_pos=[line_pos1_x, line_pos1_y],end_pos=[line_pos2_x, line_pos2_y], width=2)

    # Draw 90° - Text Markings
    img = fonts[0].render("360", True, col_mark)
    img = pygame.transform.rotate(img,0)
    screen.blit(img, (screen.get_width() / 2 - 15, 40))

    img = fonts[0].render("090", True, col_mark)
    img = pygame.transform.rotate(img,270)
    screen.blit(img, (screen.get_width() - 62, screen.get_height() / 2 - 15))

    img = fonts[0].render("180", True, col_mark)
    img = pygame.transform.rotate(img,180)
    screen.blit(img, (screen.get_width() / 2 - 15, screen.get_height() - 62))

    img = fonts[0].render("270", True, col_mark)
    img = pygame.transform.rotate(img,90)
    screen.blit(img, (40, screen.get_height() / 2 - 15))


def DrawDebugInfo(screen,fonts,mode,fps,timeouts):
    img = fonts[0].render("Mode:  " + str(mode), True, [250,250,250])
    screen.blit(img, (200,200))
    img = fonts[0].render("Rate:   " + str(fps) + "fps", True, [250,250,250])
    screen.blit(img, (200,225))
    img = fonts[0].render("Errors:  " + str(timeouts), True, [250,250,250])
    screen.blit(img, (200,250))

def DrawConfigError(screen,fonts):
        img = fonts[0].render("ERROR IN radar.cfg File", True, [255, 0, 0])
        screen.blit(img, (screen.get_width() / 2 - 100, screen.get_height() / 2))
        img = fonts[0].render("Please check configuration!", True, [255, 255, 255])
        screen.blit(img, (screen.get_width() / 2 - 115, screen.get_height() / 2 + 25))