import pygame
from pygame import gfxdraw
import Classes
import math
import Utilities
import os

opt = [False,False,False]

fonts = []

cntry_points_raw = None
cntry_points = None

surf_grid = None

def Draw(mode,screen,raw_tgts,rdr_tgts,dis_range,sweep_angle,fonts_in,opts):
    global opt, surf_grid
    global fonts

    fonts = fonts_in
    opt = opts
    
    col_back = [37,37,37]
    screen.fill(col_back)
    
    DrawCountryBorders(screen)
    
    #Draw Grid Lines
    grid_space = 100
    if opts.grid:
        if surf_grid is None:
            surf_grid = pygame.Surface((screen.get_width(), screen.get_height()),pygame.SRCALPHA)

            for i in range (-7,7):
                pygame.draw.line(surf_grid,color=[50,50,50],start_pos=[0,screen.get_height() / 2 + grid_space * i + 1],end_pos=[screen.get_width(),screen.get_height() / 2 + grid_space * i + 1],width=1)
                pygame.draw.line(surf_grid,color=[50,50,50],start_pos=[screen.get_width() / 2 + grid_space * i + 1,0],end_pos=[screen.get_width() / 2 + grid_space * i + 1,screen.get_height()],width=1)
        
        screen.blit(surf_grid,(0,0))

    conv_fact = 1
    
    if opts.metric:
        conv_fact = 1.852

    if raw_tgts is not None:
        for tgt in raw_tgts:
            if tgt.dis < dis_range * 5:
                if not tgt.drawn and sweep_angle > tgt.ang and sweep_angle <= tgt.ang + 1.2:
                    rdr_tgt = Classes.RadarTarget()
                    rdr_tgt.pos_x = screen.get_width() / 2 + math.sin(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range * conv_fact
                    rdr_tgt.pos_y = screen.get_height() / 2 - math.cos(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range * conv_fact
                    rdr_tgt.trk = tgt.trk
                    rdr_tgt.ang = tgt.ang
                    rdr_tgt.spd = tgt.spd
                    rdr_tgt.age = tgt.time
                    rdr_tgt.cls = tgt.flt

                    sze = 2
                    if tgt.cat == "A1":
                        sze = 2
                    elif tgt.cat == "A2":
                        sze = 3
                    if tgt.cat == "A3":
                        sze = 4
                    if tgt.cat == "A4":
                        sze = 4
                    if tgt.cat == "A5":
                        sze = 5
                    rdr_tgt.sze = sze

                    rdr_tgts.append(rdr_tgt)
                    raw_tgts.remove(tgt)

    if mode == 0:
        AnalogDraw1(screen,rdr_tgts,dis_range,sweep_angle)
    elif mode == 1:
        AnalogDraw2(screen,rdr_tgts,dis_range,sweep_angle)
    elif mode == 2:
        AnalogDraw3(screen,rdr_tgts,dis_range,sweep_angle)
    elif mode == 3:
        DigitalDraw(screen,rdr_tgts,dis_range,sweep_angle)

    opt.force_update = False

def AnalogDraw1(screen,rdr_tgts,dis_range,sweep_angle):
    global fonts
    col_mark = [205,205,205]
    
    #Draw Scan Bar
    for i in range (0,20):
        j = 20 - i
        line_x = screen.get_width() / 2 + math.sin((sweep_angle - j / 5) * math.pi / 180) * 540
        line_y = screen.get_height() / 2 - math.cos((sweep_angle - j / 5) * math.pi / 180) * 540
        col_scan = [39 + 11 * i / 20, 39 + 211 * i / 20, 39 + 11 * i / 20]
        pygame.draw.line(screen,color=col_scan,start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=3)

    #Draw Radar Range Lines
    for j in range (1,6):
        for i in range (0,90):
            ang = (- sweep_angle - i - 180) * math.pi / 180

            center = [screen.get_width() / 2,screen.get_height() / 2]
            rect = pygame.Rect(0, 1, 2, 3)
            rect.center = center[0] - 100 * j, center[1] - 100 * j
            rect.width = 200 * j
            rect.height = 200 * j
            col_scan = [39 + 11 * i / 90, 39 + 211 * i / 90, 39 + 11 * i / 90]
            pygame.draw.arc(screen, col_scan, rect,ang, ang + 1 * math.pi / 180, 1)
    
    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:
        if rdr_tgt.age < 10:
            col = [round(20 * rdr_tgt.fade / 1000,0) + 37, round(190 * rdr_tgt.fade / 1000,0) + 37, round(20 * rdr_tgt.fade / 1000,0) + 37]
            sta_pos_x = rdr_tgt.pos_x + math.cos(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            sta_pos_y = rdr_tgt.pos_y + math.sin(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            end_pos_x = rdr_tgt.pos_x - math.cos(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            end_pos_y = rdr_tgt.pos_y - math.sin(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            pygame.draw.line(screen,color=col,start_pos=[sta_pos_x, sta_pos_y],end_pos=[end_pos_x, end_pos_y], width=rdr_tgt.sze)

        rdr_tgt.fade = rdr_tgt.fade * 0.98
        if rdr_tgt.fade < 10:
            rdr_tgts.remove(rdr_tgt)  

    
    #Draw Center Circle
    pygame.draw.circle(screen,color=col_mark,center=[screen.get_width() / 2, screen.get_height() / 2], radius=3)


def AnalogDraw2(screen,rdr_tgts,dis_range,sweep_angle):
    global fonts
    col_mark = [205,205,205]
       
    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:
        if rdr_tgt.age < 10:
            col = [round(20 * rdr_tgt.fade / 1000,0) + 37, round(190 * rdr_tgt.fade / 1000,0) + 37, round(20 * rdr_tgt.fade / 1000,0) + 37]
            sta_pos_x = rdr_tgt.pos_x + math.cos(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            sta_pos_y = rdr_tgt.pos_y + math.sin(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            end_pos_x = rdr_tgt.pos_x - math.cos(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            end_pos_y = rdr_tgt.pos_y - math.sin(rdr_tgt.ang * math.pi / 180) * 4 * rdr_tgt.sze / 2
            pygame.draw.line(screen,color=col,start_pos=[sta_pos_x, sta_pos_y],end_pos=[end_pos_x, end_pos_y], width=rdr_tgt.sze)

        rdr_tgt.fade = rdr_tgt.fade * 0.9965
        if rdr_tgt.fade < 10:
            rdr_tgts.remove(rdr_tgt)  

    #Draw Scan Bar
    for i in range (0,20):
        j = 20 - i
        line_x = screen.get_width() / 2 + math.sin((sweep_angle - j / 5) * math.pi / 180) * 500
        line_y = screen.get_height() / 2 - math.cos((sweep_angle - j / 5) * math.pi / 180) * 500
        col_scan = [39 + 11 * i / 20, 39 + 211 * i / 20, 39 + 11 * i / 20]
        pygame.draw.line(screen,color=col_scan,start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=3)

    DrawMarkings(screen,fonts,col_mark,dis_range)

    #Draw Center Circle
    pygame.draw.circle(screen,color=col_mark,center=[screen.get_width() / 2, screen.get_height() / 2], radius=3)

def AnalogDraw3(screen,rdr_tgts,dis_range,sweep_angle):
    global fonts
    col_mark = [205,205,205]
    
    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:
        if rdr_tgt.age < 10:
            col = [round(20 * rdr_tgt.fade / 1000,0) + 37, round(190 * rdr_tgt.fade / 1000,0) + 37, round(20 * rdr_tgt.fade / 1000,0) + 37]
            pygame.draw.circle(screen,color=col,center=[rdr_tgt.pos_x, rdr_tgt.pos_y], radius=7)
        
        rdr_tgt.fade = rdr_tgt.fade * 0.9965
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
                img = fonts[0].render(rdr_tgt.cls, True, [175,175,175])
                label_offset_y = -20
                if rdr_tgt.trk >= 270 or rdr_tgt.trk <= 90:
                    label_offset_y = 10
                screen.blit(img, (rdr_tgt.pos_x - 20, rdr_tgt.pos_y + label_offset_y))

        #Remove old targets ahead of sweep bar
        if sweep_angle > rdr_tgt.ang - 1.5 and sweep_angle < rdr_tgt.ang:
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

        if opt.metric:
            range_unit ="KM"

        img = fonts[1].render(str(i * dis_range) + range_unit, True, col_mark)
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
    img = fonts[1].render("360", True, col_mark)
    img = pygame.transform.rotate(img,0)
    screen.blit(img, (screen.get_width() / 2 - img.get_width() / 2 + 2, 45))

    img = fonts[1].render("090", True, col_mark)
    img = pygame.transform.rotate(img,270)
    screen.blit(img, (screen.get_width() - 67, screen.get_height() / 2 - img.get_height() / 2 + 2))

    img = fonts[1].render("180", True, col_mark)
    img = pygame.transform.rotate(img,180)
    screen.blit(img, (screen.get_width() / 2 - img.get_width() / 2 + 2, screen.get_height() - 67))

    img = fonts[1].render("270", True, col_mark)
    img = pygame.transform.rotate(img,90)
    screen.blit(img, (45, screen.get_height() / 2 - img.get_height() / 2 + 2))


def DrawDebugInfo(screen,fonts,mode,fps,dwnl_stats,temp):
    img = fonts[1].render("Mode:  " + str(mode), True, [250,250,250])
    screen.blit(img, (200,200))
    img = fonts[1].render("Rate:   " + str(fps) + "fps", True, [250,250,250])
    screen.blit(img, (200,225))
    img = fonts[1].render("D/E/%:  " + str(dwnl_stats[0]) + " / " + str(dwnl_stats[1]) + " / " + str(round(dwnl_stats[1] / dwnl_stats[0] * 100,1)) + "%", True, [250,250,250])
    screen.blit(img, (200,250))

    #Show temp only on Rasberry Pi:
    if temp != -99:
        img = fonts[1].render("CPU Temp: " + str(round(temp,1)) + "°C", True, [250,250,250])
        screen.blit(img, (200,275))

    img = fonts[1].render("Path:  " + os.getcwd(), True, [250,250,250])
    screen.blit(img, (200,300))

def DrawConfigError(screen,fonts):
    img = fonts[1].render("ERROR IN radar.cfg File", True, [255, 0, 0])
    screen.blit(img, (screen.get_width() / 2 - 100, screen.get_height() / 2))
    img = fonts[1].render("Please check configuration!", True, [255, 255, 255])
    screen.blit(img, (screen.get_width() / 2 - 115, screen.get_height() / 2 + 25))

def DrawUI(screen,fonts,UIElement):
    if isinstance(UIElement, Classes.Button):
        DrawButton(screen,fonts,UIElement)
    elif isinstance(UIElement, Classes.Text):
        DrawTextDisplay(screen,fonts,UIElement)
    elif isinstance(UIElement, Classes.Rectangle):
        DrawRectangle(screen,UIElement)

def DrawButton(screen,fonts,button):
    #Draw Outer Rectangle
    rect = pygame.Rect([button.pos[0] - 5, button.pos[1] - 5],[button.sze[0] + 10, button.sze[1] + 10])
    pygame.draw.rect(screen,[100,100,100],rect)
    button.rect = rect

    #Draw Inner Rectangle
    rect = pygame.Rect(button.pos,button.sze)
    mousePos = pygame.mouse.get_pos()
    
    if button.high:
        if rect.collidepoint(mousePos):
            col = [0,225,0]
        else:
            col = [0,150,0]
    else:
        if rect.collidepoint(mousePos):
            col = [225,225,225]
        else:
            col = [175,175,175]
    pygame.draw.rect(screen,col,rect)

    img = fonts[1].render(button.txt, True, [0, 0, 0])
    screen.blit(img, (button.pos[0] + button.sze[0] / 2 - img.get_width() / 2,button.pos[1] + button.sze[1] / 2 - img.get_height() / 2))

def DrawTextDisplay(screen,fonts,display):
    img = fonts[display.fnt_sze].render(display.txt, True, [255, 255, 255])
    screen.blit(img, (display.pos[0] + display.sze[0] / 2 - img.get_width() / 2,display.pos[1] + display.sze[1] / 2 - img.get_height() / 2))

def DrawRectangle(screen,rectanle):
    #Draw Inner Rectangle
    s = pygame.Surface((rectanle.sze))
    s.fill(rectanle.col)
    s.set_alpha(rectanle.alpha)
    screen.blit(s,rectanle.pos)

def DrawCountryBorders(screen):
    global cntry_points_raw, cntry_points
    global opt

    col_cntry = [65,65,65]
    #Check if raw Country Points need to be loaded from file...
    if cntry_points_raw is None:
        cntry_points_raw = Utilities.loadCountryPoints()

    #Check if Country Points were loaded by previous step, if not return
    if cntry_points_raw is None:
        return

    #Check if Country Points need to be processed
    if cntry_points is None or opt.force_update:
        cntry_points = Utilities.calcCountryPoints(screen.get_size(),cntry_points_raw,opt.homePos,opt.dis_range,opt.metric)
    
    #Draw Countries
    if cntry_points is not None:
        for some_points in cntry_points:
            pygame.draw.polygon(screen,col_cntry,some_points,2)