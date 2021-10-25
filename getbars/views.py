from django.shortcuts import render
from math import radians
from django.template import context
from pprint import pprint
import requests

bars=[]
# Create your views here.

def home(request):
        return render(request, 'getbars/index.html',{
    })
def bar(request): 
    # get location 
    response = requests.get('https://freegeoip.app/json/').json()
    lat = response['latitude']
    lon = response['longitude']
    #get breweries attributed to location
    response2 = requests.get('https://api.openbrewerydb.org/breweries?by_dist='+str(lat)+','+str(lon)+"'").json()
    sun_Time=requests.get('https://api.sunrise-sunset.org/json?lat='+str(lat)+'&'+"lng="+str(lon)+"'/").json()
    sunseTime=sun_Time["results"]
    sunSet=sunseTime["sunset"]
    data={}
    k=0
    #store response
    for item in response2:
        dist = get_dist(lat, lon, float(item['latitude']), float(item['longitude']))
        if dist > 9 :
            continue
        item['distance']= dist
        pnum = item['phone']
        pformatted = formatPhone(pnum)
        item['phone']= pformatted
        data[k] = item
        k+=1
        #check responses
        print(item['website_url'] )
    #print to page
    return render(request, 'getbars/bar.html',{
        'barlist': data,
        'sunTime':sunSet
    })

def get_dist(ulat, ulong, blat, blong):
    import math
    coordlat = ulat
    coordlon = ulong
    ulat, ulong, blat, blong = map(radians, [ulat, ulong, blat, blong])
    coord2 = blat, blong
    R = 6371000 #radius of Eath in meters
    deltaphi = blat - ulat
    deltalam = blong - ulong
    a = math.sin(deltaphi/2.0)**2+ math.cos(ulat) * math.cos(blat)*math.sin(deltalam/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    miles = (R * c)* 0.000621371
    return miles

def formatPhone(x):
    if x is None:
        return "No number listed"
    elif len(x) != 10:
        return "No number listed"
    else:
        phone = x[:3]+'-'+x[3:6]+'-'+x[6:]
        return phone
