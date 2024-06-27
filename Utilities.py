import json
import math
import time
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import os

def loadCountryPoints():
    all_points = []

    path_mod = "."
    if os.name == 'posix' or os.name != 'nt':
        path_mod = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') + "/Pi-Radar/"
    
    if not os.path.exists(path_mod + '/res/countries.json'):
        return None
    
    #Load Json from file
    f = open(path_mod + '/res/countries.json')
    datas = json.load(f)
    
    #Itterate through json data to find geometries and rings
    for features in datas["features"]:
        geometry = features["geometry"]

        #Only one geometry per feature, however multiple rings possible -> each ring results in one point group
        for rings in geometry["rings"]:
            point_group = []

            #Prepare minimum and maximum buffers
            min_lat = min_lng = 999
            max_lat = max_lng = -999

            #Each ring has multiple coordinates
            for coordinates in rings:
                #Append each coordinate to the point group after doing some rounding
                point_group.append((round(coordinates[0],5),(round(coordinates[1],5))))

                #Find min and max lat&lng of each point group
                if min_lat > coordinates[0]:
                    min_lat = coordinates[0]

                if min_lng > coordinates[1]:
                    min_lng = coordinates[1]

                if max_lat < coordinates[0]:
                    max_lat = coordinates[0]

                if max_lng < coordinates[1]:
                    max_lng = coordinates[1]
        
            #Append two more "fake points" to each point group, containing mins and maximums
            point_group.append((min_lat,min_lng))
            point_group.append((max_lat,max_lng))

            all_points.append(point_group)

    return all_points


def calcCountryPoints(bounds_in,raw_points_in,pos_in,range_in,metric):
    points_out = []

    #t_start = time.time()

    range_in = range_in * 10

    #Get the maximum and minimum lat&lng of the display area
    min_lat = pos_in.lat - range_in * 1000 / 1852 / 60 / math.cos(pos_in.lat *math.pi / 180)
    min_lng = pos_in.lng - range_in * 1000 / 1852 / 60

    max_lat = pos_in.lat + range_in * 1000 / 1852 / 60 / math.cos(pos_in.lat *math.pi / 180)
    max_lng = pos_in.lng + range_in * 1000 / 1852 / 60

    if not metric:
        range_in = range_in * 1.852

    for raw_point in raw_points_in:
        point_out = []
        
        #Get the maximum and minimum lat&lng of the point group
        max_point = raw_point[len(raw_point) - 1]       
        min_point = raw_point[len(raw_point) - 2]

        #If maximum or minimum lat outside of display area, skip group
        if not max_point[1] > min_lat or not min_point[1] < max_lat:
            continue
        
        #If maximum or minimum lng outside of display area, skip group
        if not max_point[0] > min_lng or not min_point[0] < max_lng: 
            continue

        #Calculate screen postion for each point group - Skip last two raw points, as those are the max and min points of each point group
        for i in range(0,len(raw_point) - 3):
                point = raw_point[i]

                d_lat = point[1] - pos_in.lat
                d_lat = d_lat * 60
                d_lat = d_lat * 1852 / 1000
                d_lat = int(- d_lat *  bounds_in[0] / range_in + bounds_in[1] / 2)

                d_lng = point[0] - pos_in.lng
                d_lng = d_lng * 60 * math.cos(pos_in.lat * math.pi / 180)
                d_lng = d_lng * 1852 / 1000
                d_lng = int(d_lng *  bounds_in[0] / range_in + bounds_in[0] / 2)

                point_out.append((d_lng,d_lat))

        #Append point group to total list
        points_out.append(point_out)

    #print(str(time.time() - t_start))
    #Output total list
    return points_out
