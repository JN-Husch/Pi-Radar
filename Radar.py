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

version = "0.3.0"

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1080, 1080),pygame.FULLSCREEN|SCALED)
screen.set_alpha(None)
clock = pygame.time.Clock()

path_mod = ""
cpu = None
cpu_temp = -99

#Choose available fonts based on operating system
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
    from gpiozero import CPUTemperature
    cpu = CPUTemperature()

fonts = [font1,font2,font3]

mouse_down = [False,False]  #Left Mouse Button, Right Mouse Button

#mode = 1 #1 - Analog Radar, 2 - Digital Radar
sweep_angle = 270

b_key_plus_pressed = False
b_key_minus_pressed = False
menu_level = 0
UIElements = []


#Set up Options
opts = Classes.Options()
opts.vers = version
opts = Menu.LoadOptions(path_mod,opts)

rdr_tgts = []
raw_tgts = []
raw_tgts_new = []

fps = 0
dwnl_stats = [1,0] #0 - Total Downloads, #1 - Errors

run = True

#Use airplanes.live API if no url has been defined
if len(opts.url) < 2:
    opts.url = "https://api.airplanes.live/v2/point/" + str(opts.homePos.lat) + "/" + str(opts.homePos.lng) + "/250"
    opts.source = "airplanes.live API"
else:
    opts.source = "Local URL: " + opts.url

#Main Prcoessing Function
def DataProcessing():
    global raw_tgts_new
    global opts
    global dwnl_stats
    
    if opts.config_ok:
        raw_tgts_new = DataFetcher.fetchADSBData(opts.homePos,opts.url)
        dwnl_stats[0] += 1
        if raw_tgts_new is None:
            dwnl_stats[1] += 1


#Main Drawing Function and Input Handler
def DataDrawing():
    global raw_tgts, raw_tgts_new
    global run, screen, sweep_angle, menu_level
    global fps, opts, cpu_temp
    global UIElements

    while run:
        
        #Check pygame events -- massive mess - TODO: Improve!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Mouse or Touchscreen press event
            elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN) and not mouse_down[0]:              
                mouse_down[0] = True            

                mousePos = pygame.mouse.get_pos()

                if menu_level == 0:
                    menu_level = 1
                else:
                    for UIElement in UIElements:
                        if isinstance(UIElement, Classes.Button):
                            if UIElement.rect.collidepoint(mousePos):
                                #On any menu level, Return moves one level up
                                if UIElement.tag =="RETURN":
                                    if menu_level > 0:
                                        menu_level -= 1                   
                                
                                #Menu Level 1 - Main Menu
                                if menu_level == 1:
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
                                            opts.force_update = True
                                            if opts.mode == 3:
                                                rdr_tgts.clear()
                                    if UIElement.tag == "RNG_DN":
                                        if opts.dis_range >= 10:
                                            opts.dis_range = int(round(opts.dis_range / 2,0))
                                            opts.force_update = True
                                            if opts.mode == 3:
                                                rdr_tgts.clear()
                                    if UIElement.tag == "OPTIONS":
                                        menu_level = 2

                                #Menu Level 2 - Options
                                elif menu_level == 2:
                                    if "DEBUG" in UIElement.tag:
                                       opts.debug = UIElement.tag.split("_")[1] == "True"

                                    if "GRID" in UIElement.tag:
                                        opts.grid = UIElement.tag.split("_")[1] == "True"
                                        opts.force_update = True

                                    if "METRIC" in UIElement.tag:
                                        opts.metric = UIElement.tag.split("_")[1] == "True"
                                        opts.force_update = True

                                    if "COUNTRIES" in UIElement.tag:
                                        opts.show_countries = UIElement.tag.split("_")[1] == "True"
                                        opts.force_update = True

                                    if "SAVE" in UIElement.tag:
                                        Menu.SaveOptions(path_mod,opts)            

            #Mouse or Touchscreen release event
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                mouse_down[0] = False

        #Handle keyboard buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PLUS] and opts.dis_range <= 20:
            if not b_key_plus_pressed:
                opts.dis_range = opts.dis_range * 2
                opts.force_update = True
                b_key_plus_pressed = True
                if opts.mode == 3:
                    rdr_tgts.clear()
        else:
            b_key_plus_pressed = False
        
        if keys[pygame.K_MINUS] and opts.dis_range >= 10:
            if not b_key_minus_pressed:
                opts.dis_range = int(round(opts.dis_range / 2,0))
                opts.force_update = True
                b_key_minus_pressed = True
                if opts.mode == 3:
                    rdr_tgts.clear()
        else:
            b_key_minus_pressed = False

        #Call main drawing function if config is okay, else draw config error
        if opts.config_ok:
            Drawer.Draw(opts.mode,screen,raw_tgts,rdr_tgts,opts.dis_range,sweep_angle,fonts,opts)
            if opts.debug:
                Drawer.DrawDebugInfo(screen,fonts,opts.mode,fps,dwnl_stats,cpu_temp)
        else:
            Drawer.DrawConfigError(screen,fonts)            

        #Show Menu UI
        if menu_level != 0:
            UIElements = Menu.Main(screen,menu_level,opts)
            for UIElement in UIElements:
                Drawer.DrawUI(screen,fonts,UIElement)

        #Adjust sweep angle by so many degrees each frame
        sweep_angle += 1.2

        #Handle sweep angle overflow and start a new download task
        if sweep_angle > 359:
            raw_tgts = raw_tgts_new
            raw_tgts_new = None
            sweep_angle = 0
            t2 = threading.Thread(target=task1)
            t2.start()

        #At 180° check if the first downlaod task has resulted in a successfull data download, if not restart
        if raw_tgts_new is None:
            if sweep_angle > 180 and sweep_angle <= 180 + 1.2:
                t3 = threading.Thread(target=task1)
                t3.start()
        
        #Show data on the pygame screen
        pygame.display.flip()
        dt = clock.tick(30) / 1000
        fps = round(clock.get_fps(),0)

#Task 1 - Download and process data
def task1():
    DataProcessing()

t1 = threading.Thread(target=task1)
t1.start()

#Task 2 - Check CPU temperature on UNIX system
def task2():
    global cpu,cpu_temp
    while run:
        cpu_temp = cpu.temperature  
        time.sleep(1)

if os.name == 'posix':
    t2 = threading.Thread(target=task2)
    t2.start()

#Start the drawing loop
DataDrawing()

#If breaking out of above loop, save options and shutdown pygame gracefully
Menu.SaveOptions(path_mod,opts)
pygame.quit()



