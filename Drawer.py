import pygame
from pygame import gfxdraw
import Classes
import math

def Draw(mode,screen,raw_tgts,rdr_tgts,dis_range,sweep_angle,font):
    
    if raw_tgts is not None:
        for tgt in raw_tgts:
            if tgt.dis < dis_range * 5:
                if not tgt.drawn and sweep_angle > tgt.ang and sweep_angle < tgt.ang + 1:
                    rdr_tgt = Classes.RadarTarget()
                    rdr_tgt.pos_x = screen.get_width() / 2 + math.sin(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range
                    rdr_tgt.pos_y = screen.get_height() / 2 - math.cos(tgt.ang * math.pi / 180) * tgt.dis * 100 / dis_range
                    rdr_tgt.trk = tgt.trk
                    rdr_tgt.ang = tgt.ang
                    rdr_tgt.spd = tgt.spd
                    rdr_tgt.age = tgt.time
                    rdr_tgt.cls = tgt.flt
                    rdr_tgts.append(rdr_tgt)
                    #tgt.drawn = True
                    raw_tgts.remove(tgt)
    if mode == 1:
        AnalogDraw(screen,rdr_tgts,dis_range,sweep_angle,font)
    elif mode == 2:
        DigitalDraw(screen,rdr_tgts,dis_range,sweep_angle,font)

def AnalogDraw(screen,rdr_tgts,dis_range,sweep_angle,fonts):
    screen.fill([37,37,37])

    #Handle Radar Targets
    for rdr_tgt in rdr_tgts:
        if rdr_tgt.age < 10:
            col = [round(20 * rdr_tgt.fade / 1000,0) + 37, round(190 * rdr_tgt.fade / 1000,0) + 37, round(20 * rdr_tgt.fade / 1000,0) + 37]
            pygame.draw.circle(screen,color=col,center=[rdr_tgt.pos_x, rdr_tgt.pos_y], radius=7)
        
        rdr_tgt.fade = rdr_tgt.fade * 0.997
        if rdr_tgt.fade < 10:
            rdr_tgts.remove(rdr_tgt)
    
    #Draw range circles
    for i in range(1,6):
        gfxdraw.aacircle(screen,int(screen.get_width() / 2), int(screen.get_height() / 2), 100 * i,[50, 205, 50])
        img = fonts[0].render(str(i * dis_range) + "NM", True, [50, 205, 50])
        screen.blit(img, (screen.get_width() / 2 - 20, screen.get_height() / 2 + 100 * i + 10))
    
    #Draw indexes
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
            pygame.draw.line(screen,color=[50, 205, 50],start_pos=[line_pos1_x, line_pos1_y],end_pos=[line_pos2_x, line_pos2_y], width=2)

    #Draw Scan Bar
    line_x = screen.get_width() / 2 + math.sin(sweep_angle * math.pi / 180) * 540
    line_y = screen.get_height() / 2 - math.cos(sweep_angle * math.pi / 180) * 540
    pygame.draw.line(screen,color=[50, 250, 50],start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=2)
    
    #Draw Center Circle
    pygame.draw.circle(screen,color=[50, 205, 50],center=[screen.get_width() / 2, screen.get_height() / 2], radius=3)



def DigitalDraw(screen,rdr_tgts,dis_range,sweep_angle,fonts):
    screen.fill([37,37,37])
 
    #Draw range circles
    for i in range(1,6):
        gfxdraw.aacircle(screen,int(screen.get_width() / 2), int(screen.get_height() / 2), 100 * i,[75, 75, 75])
        img = fonts[0].render(str(i * dis_range) + "NM", True, [100, 100, 100])
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
            pygame.draw.line(screen,color=[75, 75, 75],start_pos=[line_pos1_x, line_pos1_y],end_pos=[line_pos2_x, line_pos2_y], width=2)
    
    for i in range (0,4):
        angle = i * 90
        line_pos1_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (5) 
        line_pos1_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (5)
        line_pos2_x = screen.get_width() / 2 + math.sin(angle * math.pi / 180) * (10)
        line_pos2_y = screen.get_height() / 2 - math.cos(angle * math.pi / 180) * (10)
        pygame.draw.line(screen,color=[75, 75, 75],start_pos=[line_pos1_x, line_pos1_y],end_pos=[line_pos2_x, line_pos2_y], width=2)
    
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
        if sweep_angle > rdr_tgt.ang - 5 and sweep_angle < rdr_tgt.ang:
            rdr_tgts.remove(rdr_tgt) 

    #Draw Scan Bar
    line_x = screen.get_width() / 2 + math.sin(sweep_angle * math.pi / 180) * 500
    line_y = screen.get_height() / 2 - math.cos(sweep_angle * math.pi / 180) * 500
    pygame.draw.line(screen,color=[50, 205, 50],start_pos=[screen.get_width() / 2, screen.get_height() / 2],end_pos=[line_x, line_y], width=2)
