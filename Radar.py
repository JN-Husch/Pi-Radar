import pygame
from pygame import gfxdraw
import time
import math
import DataFetcher
import Classes
import Drawer
import threading
import os
import shutil
from pygame.locals import *

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1080, 1080),pygame.FULLSCREEN|SCALED)
clock = pygame.time.Clock()
dt = 0

path_mod = ""

if os.name != 'nt':
    path_mod = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') + "/Radar/"
    #pygame.mouse.set_visible(False)


font1 = pygame.font.Font(path_mod + "res/Arial.ttf", 20)
font2 = pygame.font.Font(path_mod + "res/Arial.ttf", 12)
fonts = [font1,font2]

mouse_down = [False,False]

t0 = time.time()

mode = 1 #1 - Analog Radar, 2 - Digital Radar
sweep_angle = 270
dis_range = 10

b_key_plus_pressed = False
b_key_minus_pressed = False


opts = [False, False, False]  #0 - Debug Info, 1 - Draw Grid Lines, 2 - Use Metric

homePos = Classes.HomePosition()

rdr_tgts = []
raw_tgts = []
raw_tgts_new = []

fps = 0
timeouts = 0

run = True
config_ok = False

if os.path.exists(path_mod + 'radar.cfg'):
    with open(path_mod + 'radar.cfg') as f:
        lines = f.readlines()
    try:
        if len(lines) > 0:
            for line in lines:
                if "FEEDER_URL=" in line:
                    url = line.split("=")[1].replace("\"","").strip()
                if "RADAR_MODE=" in line:
                    mode = int(line.split("=")[1].strip())
                if "LAT=" in line:
                    homePos.lat = float(line.split("=")[1].strip())
                if "LNG=" in line:
                    homePos.lng = float(line.split("=")[1].strip())
                if "RANGE=" in line:
                    zoom = int(line.split("=")[1].strip())
                    if zoom == 2:
                        dis_range = 10
                    elif zoom == 3:
                        dis_range = 20
                    elif zoom == 4:
                        dis_range == 40
                    else:
                        dis_range = 5
                if "DEBUG=" in line:
                    if line.split("=")[1].lower().strip() == "true":
                        opts[0] = True
                if "GRID_LINES=" in line:
                    if line.split("=")[1].lower().strip() == "true":
                        opts[1] = True
                if "RANGE_IN_KM=" in line:
                    if line.split("=")[1].lower().strip() == "true":
                        opts[2] = True

        config_ok = True

    except:
        print("Error reading radar.cfg!")
else:
    print("radar.cfg does not exist!")

def DataProcessing():
    global raw_tgts_new
    global opts
    global timeouts
    
    if config_ok:
        raw_tgts_new = DataFetcher.fetchADSBData(homePos,url)
        if raw_tgts_new is None:
            timeouts += 1

def DataDrawing():
    global raw_tgts
    global raw_tgts_new
    global run
    global dis_range
    global sweep_angle
    global screen
    global fps
    global mode
    global opts 
    global timeouts

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if config_ok:
            Drawer.Draw(mode,screen,raw_tgts,rdr_tgts,dis_range,sweep_angle,fonts,opts)
            if opts[0]:
                Drawer.DrawDebugInfo(screen,fonts,mode,fps,timeouts)
        else:
            Drawer.DrawConfigError(screen,fonts)
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PLUS] and dis_range <= 20:
            if not b_key_plus_pressed:
                dis_range = dis_range * 2
                b_key_plus_pressed = True
                if mode == 2:
                    rdr_tgts.clear()
        else:
            b_key_plus_pressed = False
        if keys[pygame.K_MINUS] and dis_range >= 10:
            if not b_key_minus_pressed:
                dis_range = int(round(dis_range / 2,0))
                b_key_minus_pressed = True
                if mode == 2:
                    rdr_tgts.clear()
        else:
            b_key_minus_pressed = False
        
        pygame.display.flip()
        dt = clock.tick(40) / 1000

        fps = round(clock.get_fps(),0)

        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_down[0]:
            mouse_down[0] = True
            if mouse_pos[0] > screen.get_width() / 2:
                mode += 1
            else:
                mode -= 1
            rdr_tgts.clear()
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down[0] = False
        
        sweep_angle += 0.9
        if raw_tgts_new is None:
            if sweep_angle > 180 and sweep_angle < 180 + 40 * dt:
                t3 = threading.Thread(target=task1)
                t3.start()
        
        if sweep_angle > 359:
            raw_tgts = raw_tgts_new
            raw_tgts_new = None
            sweep_angle = 0
            t2 = threading.Thread(target=task1)
            t2.start()

def task1():
    DataProcessing()

t1 = threading.Thread(target=task1)
t1.start()

DataDrawing()

pygame.quit()