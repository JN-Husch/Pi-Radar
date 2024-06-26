import pygame
from pygame import gfxdraw
from pygame.locals import *
import time
import math
import DataFetcher
import Classes
import Drawer
import Menu
import threading
import os

version = "0.2.0"

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1080, 1080),pygame.FULLSCREEN|SCALED)
clock = pygame.time.Clock()
dt = 0

path_mod = ""

if os.name == 'nt':
    font1 = pygame.font.SysFont('ocrastdopentype', 15)
    font2 = pygame.font.SysFont('ocrastdopentype', 20)
    font3 = pygame.font.SysFont('ocrastdopentype', 25)
elif os.name == 'posix' or os.name != 'nt':
    path_mod = os.path.join(os.path.join(os.path.expanduser('~')), '.config') + "/pi-radar/"
    pygame.mouse.set_visible(False)
    font1 = pygame.font.SysFont('quicksand', 15)
    font2 = pygame.font.SysFont('quicksand', 20)
    font3 = pygame.font.SysFont('quicksand', 25)

fonts = [font1,font2,font3]

mouse_down = [False,False]

t0 = time.time()

#mode = 1 #1 - Analog Radar, 2 - Digital Radar
sweep_angle = 270

b_key_plus_pressed = False
b_key_minus_pressed = False


opts = Classes.Options()
opts.vers = version

rdr_tgts = []
raw_tgts = []
raw_tgts_new = []

fps = 0
dwnl_stats = [1,0] #0 - Total Downloads, #1 - Errors

menu_modes = [False,0,0] #0 - Open, 
menu_level = 0

run = True
UIElements = []

opts = Menu.LoadOptions(path_mod,opts)

#Use airplanes.live API if no url has been defined
if len(opts.url) < 2:
    opts.url = "https://api.airplanes.live/v2/point/" + str(opts.homePos.lat) + "/" + str(opts.homePos.lng) + "/250"
    opts.source = "airplanes.live API"
else:
    opts.source = "Local URL: " + opts.url

def Stop():
    global run
    run = False

def DataProcessing():
    global raw_tgts_new
    global opts
    global dwnl_stats
    
    if opts.config_ok:
        raw_tgts_new = DataFetcher.fetchADSBData(opts.homePos,opts.url)
        dwnl_stats[0] += 1
        if raw_tgts_new is None:
            dwnl_stats[1] += 1

def DataDrawing():
    global raw_tgts, raw_tgts_new
    global run, screen, sweep_angle, menu_modes
    global fps, opts
    global UIElements

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if opts.config_ok:
            Drawer.Draw(opts.mode,screen,raw_tgts,rdr_tgts,opts.dis_range,sweep_angle,fonts,opts)
            if opts.debug:
                Drawer.DrawDebugInfo(screen,fonts,opts.mode,fps,dwnl_stats)
        else:
            Drawer.DrawConfigError(screen,fonts)            
        
        if menu_modes[0]:
            UIElements = Menu.Main(screen,menu_level,opts)
            for UIElement in UIElements:
                Drawer.DrawUI(screen,fonts,UIElement)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_PLUS] and opts.dis_range <= 20:
            if not b_key_plus_pressed:
                opts.dis_range = opts.dis_range * 2
                b_key_plus_pressed = True
                if opts.mode == 3:
                    rdr_tgts.clear()
        else:
            b_key_plus_pressed = False
        
        if keys[pygame.K_MINUS] and opts.dis_range >= 10:
            if not b_key_minus_pressed:
                opts.dis_range = int(round(opts.dis_range / 2,0))
                b_key_minus_pressed = True
                if opts.mode == 3:
                    rdr_tgts.clear()
        else:
            b_key_minus_pressed = False
        
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

        pygame.display.flip()
        dt = clock.tick(40) / 1000
        fps = round(clock.get_fps(),0)

        
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN) and not mouse_down[0]:              
            mouse_down[0] = True            


            mousePos = pygame.mouse.get_pos()

            if not menu_modes[0]:
                menu_modes[0] = True
                menu_level = 0
            else:
                for UIElement in UIElements:
                    if isinstance(UIElement, Classes.Button):
                        if UIElement.rect.collidepoint(mousePos):
                            if UIElement.tag =="RETURN":
                                if menu_level > 0:
                                    menu_level -= 1
                                else:
                                    menu_modes[0] = False                        
                            if menu_level == 0:
                                if UIElement.tag == "EXIT":
                                    run = False
                                if UIElement.tag == "MODE_UP":
                                    if opts.mode < 3:
                                        opts.mode += 1
                                        rdr_tgts.clear()
                                if UIElement.tag == "MODE_DN":
                                    if opts.mode > 0:
                                        opts.mode -= 1
                                        rdr_tgts.clear()
                                if UIElement.tag == "RNG_UP":
                                    if opts.dis_range <= 20:
                                        opts.dis_range = opts.dis_range * 2
                                        if opts.mode == 3:
                                            rdr_tgts.clear()
                                if UIElement.tag == "RNG_DN":
                                    if opts.dis_range >= 10:
                                        opts.dis_range = int(round(opts.dis_range / 2,0))
                                        if opts.mode == 3:
                                            rdr_tgts.clear()
                                if UIElement.tag == "OPTIONS":
                                    menu_level = 1
                            elif menu_level == 1:
                                if "DEBUG" in UIElement.tag:
                                   opts.debug = UIElement.tag.split("_")[1] == "True"

                                if "GRID" in UIElement.tag:
                                    opts.grid = UIElement.tag.split("_")[1] == "True"

                                if "METRIC" in UIElement.tag:
                                    opts.metric = UIElement.tag.split("_")[1] == "True"

                                if "SAVE" in UIElement.tag:
                                    Menu.SaveOptions(path_mod,opts)            

        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
            mouse_down[0] = False

def task1():
    DataProcessing()

t1 = threading.Thread(target=task1)
t1.start()

DataDrawing()

Menu.SaveOptions(path_mod,opts)
pygame.quit()



