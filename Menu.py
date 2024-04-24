import pygame
import Classes
import os


fonts = []

level = 0

def Main(screen,fonts_in,level,opts):
    global fonts
    fonts = fonts_in

    if level == 0:
        return Level0(screen)
    elif level == 1:
        return Level1(screen,opts)

def Level0(screen):

    but_rng_dec = Classes.Button("RANGE DECR",[screen.get_width() / 2 - 200,200],[190, 80],"RNG_DN")
    but_rng_inc = Classes.Button("RANGE INCR",[screen.get_width() / 2 + 10,200],[190, 80],"RNG_UP")
    but_dn = Classes.Button("<<< MODE",[screen.get_width() / 2 - 200,300],[190, 80],"MODE_DN")
    but_up = Classes.Button("MODE >>>",[screen.get_width() / 2 + 10,300],[190, 80],"MODE_UP")
    but_opt = Classes.Button("OPTIONS",[screen.get_width() / 2 - 200,700],[400, 80], "OPTIONS")
    but_retu = Classes.Button("RETURN",[screen.get_width() / 2 - 200,800],[400, 80],"RETURN")
    but_exit = Classes.Button("EXIT",[screen.get_width() / 2 - 200,900],[400, 80],"EXIT")

    UIElements = []
    UIElements.append(but_up)
    UIElements.append(but_dn)
    UIElements.append(but_retu)
    UIElements.append(but_opt)
    UIElements.append(but_rng_inc)
    UIElements.append(but_rng_dec)
    UIElements.append(but_exit)

    return UIElements


def Level1(screen,opts):
    but_metric_off = Classes.Button("NAUTICAL",[screen.get_width() / 2 - 200,200],[190, 80],"METRIC_False", not opts.metric)
    but_metric_on = Classes.Button("METRIC",[screen.get_width() / 2 + 10,200],[190, 80],"METRIC_True", opts.metric)
    
    but_grid_off = Classes.Button("GRID OFF",[screen.get_width() / 2 - 200,300],[190, 80],"GRID_False",not opts.grid)
    but_grid_on = Classes.Button("GRID ON",[screen.get_width() / 2 + 10,300],[190, 80],"GRID_True", opts.grid)

    but_debug_off = Classes.Button("DEBUG OFF",[screen.get_width() / 2 - 200,400],[190, 80],"DEBUG_False",not opts.debug)
    but_debug_on = Classes.Button("DEBUG ON",[screen.get_width() / 2 + 10,400],[190, 80],"DEBUG_True", opts.debug)

    but_save = Classes.Button("SAVE",[screen.get_width() / 2 - 200,700],[400, 80],"SAVE")

    but_retu = Classes.Button("RETURN",[screen.get_width() / 2 - 200,800],[400, 80],"RETURN")

    UIElements = []
    UIElements.append(but_metric_off)
    UIElements.append(but_metric_on)    
    UIElements.append(but_grid_off)
    UIElements.append(but_grid_on)
    UIElements.append(but_debug_off)
    UIElements.append(but_debug_on)  
    #UIElements.append(but_save)
    UIElements.append(but_retu)
    return UIElements


def LoadOptions(path_mod,opts):
    if os.path.exists(path_mod + 'radar.cfg'):
        try:
            with open(path_mod + 'radar.cfg') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    for line in lines:
                        if "FEEDER_URL=" in line:
                            opts.url = line.split("=")[1].replace("\"","").strip()
                        if "RADAR_MODE=" in line:
                            opts.mode = int(line.split("=")[1].strip())
                        if "LAT=" in line:
                            opts.homePos.lat = float(line.split("=")[1].strip())
                        if "LNG=" in line:
                            opts.homePos.lng = float(line.split("=")[1].strip())
                        if "RANGE=" in line:
                            zoom = int(line.split("=")[1].strip())
                            if zoom == 2:
                                opts.dis_range = 10
                            elif zoom == 3:
                                opts.dis_range = 20
                            elif zoom == 4:
                                opts.dis_range == 40
                            else:
                                opts.dis_range = 5
                        if "DEBUG=" in line:
                            opts.debug = line.split("=")[1].lower().strip() == "true"
                        if "GRID_LINES=" in line:
                            opts.grid = line.split("=")[1].lower().strip() == "true"
                        if "RANGE_IN_KM=" in line:
                            opts.metric = line.split("=")[1].lower().strip() == "true"

                opts.config_ok = True

        except Exception as err:
            print("Error reading radar.cfg!")
            print(f"Unexpected {err=}, {type(err)=}")
    else:
        print("radar.cfg does not exist!")
    return opts

def SaveOptions(path_mod,opts):
    if os.path.exists(path_mod + 'radar.cfg'):
        
        try:
            with open(path_mod + 'radar.cfg', "r+") as f:
                lines = f.readlines()
        

                if len(lines) > 0:
                    for i in range(0,len(lines)):
                        if "FEEDER_URL=" in lines[i]:
                            lines[i] = "FEEDER_URL=" + opts.url + "\n"

                        if "RADAR_MODE=" in lines[i]:
                            lines[i] = "RADAR_MODE=" + str(opts.mode) + "\n"

                        if "LAT=" in lines[i]:
                            lines[i] = "LAT=" + str(opts.homePos.lat) + "\n"

                        if "LNG=" in lines[i]:
                            lines[i] = "LNG=" + str(opts.homePos.lng) + "\n"    

                        if "RANGE=" in lines[i]:
                            zoom = 1
                            if opts.dis_range == 10:
                                zoom = 2
                            elif opts.dis_range == 20:
                                zoom = 3
                            elif opts.dis_range == 40:
                                zoom = 4                        
                            lines[i] = "RANGE=" + str(zoom) + "\n"

                        if "DEBUG=" in lines[i]:
                            lines[i] = "DEBUG=" + str(opts.debug) + "\n"

                        if "GRID_LINES=" in lines[i]:
                            lines[i] = "GRID_LINES=" + str(opts.grid) + "\n"

                        if "RANGE_IN_KM=" in lines[i]:
                            lines[i] = "RANGE_IN_KM=" + str(opts.metric) + "\n"
                f.seek(0)
                f.truncate(0)
                f.writelines(lines)
                f.close()

        
        except Exception as err:
            print("Error writing radar.cfg!")
            print(f"Unexpected {err=}, {type(err)=}")
    pass