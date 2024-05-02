import math
import Classes
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

#Get ADSB Data from url
def fetchADSBData(homePos,url):
    tgts = []

    try:
        r = requests.get(url, timeout=4)
        aircraft_data = r.json()

        #Check if data is from local receiver or airplanes.live API by checking if it contains "ac" or "aircraft"
        var_name = "ac"
        if "aircraft" in str(aircraft_data).split(":[")[0]:
            var_name = "aircraft"

        for a in aircraft_data[var_name]:
            timestmp = aircraft_data.get("now")

            tgt = Classes.Aircraft()

            tgt.hex = a.get("hex")
            tgt.lat = a.get("lat")
            tgt.lng = a.get("lon")
            tgt.flt = a.get("flight")
            tgt.alt = a.get("alt_geom")
            tgt.spd = a.get("gs")
            tgt.trk = a.get("track")
            tgt.cat = a.get("category")

            seen_pos = a.get("seen_pos")

            #Some cleanup to prevent invalid variables being passed on:
            if tgt.reg is None or len(tgt.reg) < 1:
                tgt.reg = tgt.hex

            if tgt.flt is None:
                tgt.flt = tgt.reg

            if tgt.swk is None:
                tgt.swk = 9999

            if tgt.alt is None:
                tgt.alt = -999

            if tgt.spd is None:
                tgt.spd = -999

            if tgt.trk is None:
                tgt.trk = -999

            if tgt.lat is None:
                tgt.lat = -999        

            if tgt.lng is None:
                tgt.lng = -999    

            if seen_pos is None:
                seen_pos = 0

            tgt.time = seen_pos

            if tgt.alt !=-999 and tgt.lat != -999 and tgt.lng != -999 and tgt.spd != -999:
                vector = AngleCalc(homePos,tgt.alt,tgt.lat,tgt.lng)
                tgt.dis = round(vector[0] / 1852,3)
                tgt.ang = round(vector[1],1)
                tgts.append(tgt)
           

        return tgts
    except Exception as error:
        print("Data Download Error: ", error)
        return None

#Calculate Angle and slant range
def AngleCalc(homePos,alt_buff, lat_buff, lng_buff):
    dis_2D = 999.9

    d_lat = lat_buff - homePos.lat
    d_lng = lng_buff - homePos.lng

    d_lat = d_lat*60
    d_lng = d_lng*60*math.cos(homePos.lat *math.pi / 180)

    d_lat = d_lat * 1852
    d_lng = d_lng * 1852

    d_dis = math.sqrt(d_lat*d_lat + d_lng*d_lng)
    dis_2D = d_dis

    azi = math.acos(d_lat / dis_2D) * 180 / math.pi

    if d_lng < 0:
        azi = 360 - azi
    else:
        azi = azi

    return [dis_2D, azi]