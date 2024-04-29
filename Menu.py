import pygame
import Classes
import os

opts = Classes.Options()

def Main(screen,level,opts_in):
    global opts
    opts = opts_in

    if level == 0:
        return Level0(screen)
    elif level == 1:
        return Level1(screen)

def Level0(screen):
    global opts

    range_unit = "NM"
    if opts.metric:
        range_unit = "KM"

    UIElements = []
    UIElements.append(Classes.Rectangle([0,0,0],150,[0,0],[screen.get_width(), screen.get_height()]))
    UIElements.append(Classes.Text("MAIN MENU",[screen.get_width() / 2 - 210,115],[420, 80],fnt_sze=2))

    UIElements.append(Classes.Text("RANGE:",[screen.get_width() / 2 - 200,215],[100, 80],fnt_sze=2))
    UIElements.append(Classes.Text(str(opts.dis_range * 5) + range_unit,[screen.get_width() / 2 - 100,215],[300, 80],fnt_sze=2))

    UIElements.append(Classes.Button("RANGE DECR",[screen.get_width() / 2 - 200,300],[190, 80],"RNG_DN"))
    UIElements.append(Classes.Button("RANGE INCR",[screen.get_width() / 2 + 10,300],[190, 80],"RNG_UP"))
    UIElements.append(Classes.Text("MODE:",[screen.get_width() / 2 - 200,415],[100, 80],fnt_sze=2))
    UIElements.append(Classes.Text(getModeName(opts.mode),[screen.get_width() / 2 - 100,415],[300, 80],fnt_sze=2))
    if opts.mode > 0:
        UIElements.append(Classes.Button("<<< MODE",[screen.get_width() / 2 - 200,500],[190, 80],"MODE_DN"))
    if opts.mode < 3:
        UIElements.append(Classes.Button("MODE >>>",[screen.get_width() / 2 + 10,500],[190, 80],"MODE_UP"))
    UIElements.append(Classes.Button("OPTIONS",[screen.get_width() / 2 - 200,700],[400, 80], "OPTIONS"))
    UIElements.append(Classes.Button("RETURN",[screen.get_width() / 2 - 200,800],[400, 80],"RETURN"))
    UIElements.append(Classes.Button("EXIT",[screen.get_width() / 2 - 200,900],[400, 80],"EXIT"))
    UIElements.append(Classes.Text("Version: " + opts.vers,[screen.get_width() / 2 - 200,975],[400, 80],fnt_sze=1))

    return UIElements


def Level1(screen):
    global opts

    UIElements = []
    UIElements.append(Classes.Rectangle([0,0,0],150,[0,0],[screen.get_width(), screen.get_height()]))
    UIElements.append(Classes.Text("OPTIONS",[screen.get_width() / 2 - 210,115],[420, 80],fnt_sze=2))
    
    UIElements.append(Classes.Button("NAUTICAL",[screen.get_width() / 2 - 200,200],[190, 80],"METRIC_False", not opts.metric))
    UIElements.append(Classes.Button("METRIC",[screen.get_width() / 2 + 10,200],[190, 80],"METRIC_True", opts.metric))

    UIElements.append(Classes.Button("GRID OFF",[screen.get_width() / 2 - 200,300],[190, 80],"GRID_False",not opts.grid))
    UIElements.append(Classes.Button("GRID ON",[screen.get_width() / 2 + 10,300],[190, 80],"GRID_True", opts.grid))

    UIElements.append(Classes.Button("DEBUG OFF",[screen.get_width() / 2 - 200,400],[190, 80],"DEBUG_False",not opts.debug))
    UIElements.append(Classes.Button("DEBUG ON",[screen.get_width() / 2 + 10,400],[190, 80],"DEBUG_True", opts.debug))

    #UIElements.append(Classes.Button("SAVE",[screen.get_width() / 2 - 200,700],[400, 80],"SAVE"))
    
    UIElements.append(Classes.Text("Data Source:",[screen.get_width() / 2 - 200,650],[400, 80],fnt_sze=1))
    UIElements.append(Classes.Text(opts.source,[screen.get_width() / 2 - 200,700],[400, 80],fnt_sze=1))
    UIElements.append(Classes.Button("RETURN",[screen.get_width() / 2 - 200,800],[400, 80],"RETURN"))

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
                        if "api.airplanes.live" not in opts.url:
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


def getModeName(mode):
    name = "EMPTY"

    if mode == 0:
        name = "BASIC ANALOG"
    elif mode == 1:
        name = "ADVANCED ANALOG"
    elif mode == 2:
        name = "ANALOG DOTS"
    elif mode == 3:
        name = "DIGITAL"
    
    return name