from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
# Create your views here.
from django.conf import settings
import math
import requests
import json
import foursquare

DATASET = pd.read_csv("population_AS44_2018-10-01.csv")
DATASET=DATASET.round(6)

def home(request):
    key=settings.BING_MAPS_KEY
    return render(request,"location_module/home.html",{"key":key})


def get_population_density(request):
    latitude = round(float(request.GET.get('latitude')),6)
    longitude = round(float(request.GET.get('longitude')),6)
    # radius = int(request.GET.get('radius'))
    radius=[1,2,5]
    new_data = DATASET[DATASET['longitude'] > longitude-0.1][DATASET['longitude'] < longitude+0.1][DATASET['latitude'] > latitude-0.1][DATASET['latitude'] < latitude+0.1]
    arr=[]
    population=[0,0,0]
    for index, row in new_data.iterrows():
        d = 2*math.asin(math.sqrt((math.sin((math.radians(latitude)-math.radians(row['latitude']))/2))**2 +math.cos(math.radians(latitude))*math.cos(math.radians(row['latitude']))*(math.sin((math.radians(longitude)-math.radians(row['longitude']))/2))**2))
        d=d*6371
        if d<=radius[0]:
            population[0]+=row['population_2020']
        elif d<=radius[1]:
            population[1]+=row['population_2020']
        elif d<=radius[2]:
            population[2]+=row['population_2020']


    return render(request,"location_module/ajax/return_population.html",{"population":population})
    # queryset = DATASET[DATASET['longitude']==longitude][DATASET['latitude']==latitude]
    #
    # fin_dic={}
    # if len(queryset)==0:
    #     new_queryset = DATASET[DATASET['longitude'] > longitude-0.1][DATASET['longitude'] < longitude+0.1][DATASET['latitude'] > latitude-0.1][DATASET['latitude'] < latitude+0.1]
    #     if len(new_queryset) == 0:
    #         return render(request,"location_module/ajax/return_population.html",{"data":fin_dic})
    #     else:
    #         for index, row in new_queryset.iterrows():
    #             fin_dic[index]={}
    #             fin_dic[index]['latitude']=row['latitude']
    #             fin_dic[index]['longitude']=row['longitude']
    #             fin_dic[index]['population_2020']=row['population_2020']
    #         return render(request,"location_module/ajax/return_population.html",{"data":fin_dic})
    #
    # for index, row in queryset.iterrows():
    #     fin_dic[index]={}
    #     fin_dic[index]['latitude']=row['latitude']
    #     fin_dic[index]['longitude']=row['longitude']
    #     fin_dic[index]['population_2020']=row['population_2020']
    #
    # return render(request,"location_module/ajax/return_population.html",{"data":fin_dic})


location_type={'groceries':"4bf58dd8d48988d118951735",'pharmacies':"4bf58dd8d48988d10f951735","supermarkets":"52f2ab2ebcbc57f1066b8b46","medical_centers":"4bf58dd8d48988d104941735"}

client = foursquare.Foursquare(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET)

def get_locations(request):
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")
    ll=latitude+","+longitude
    radius = int(request.GET.get("radius"))*1000
    type = request.GET.get("type")

    if type=="groceries":
        return get_groceries(request,ll,radius,type)
    elif type=="pharmacies":
        return get_pharmacies(request,ll,radius,type)

def get_groceries(request,ll,radius,type):
    count_groceries=0
    locations=client.venues.search(params={'ll': ll, 'radius':radius, 'categoryId':location_type[type]})
    groceries={}
    for location in locations['venues']:
        groceries[count_groceries]={}
        groceries[count_groceries]["name"]=location["name"]
        groceries[count_groceries]["location"]=location["location"]
        groceries[count_groceries]["distance"]=int(location["location"]["distance"])
        groceries[count_groceries]["address"]=location["location"]["formattedAddress"]
        # cat_arr=[]
        # for cat in location["categories"]:
        #     cat_arr.append(cat["name"])
        # fin_dic[count]["categories"] = cat_arr
        count_groceries+=1
    groceries = sorted(groceries.items(), key = lambda x: x[1]['distance'])

    count_supermarkets=0
    supermarkets={}
    locations=client.venues.search(params={'ll': ll, 'radius':radius, 'categoryId':location_type["supermarkets"]})
    for location in locations['venues']:
        supermarkets[count_supermarkets]={}
        supermarkets[count_supermarkets]["name"]=location["name"]
        supermarkets[count_supermarkets]["location"]=location["location"]
        supermarkets[count_supermarkets]["distance"]=int(location["location"]["distance"])
        supermarkets[count_supermarkets]["address"]=location["location"]["formattedAddress"]
        count_supermarkets+=1
    supermarkets = sorted(supermarkets.items(), key = lambda x: x[1]['distance'])

    return render(request,"location_module/ajax/return_groceries_location.html",{"total":len(supermarkets)+len(groceries),"radius":radius,"supermarkets":supermarkets[:5],"count_supermarkets":count_supermarkets,"groceries":groceries[:5],"count_groceries":count_groceries})

def get_pharmacies(request,ll,radius,type):
    count_pharmacies=0
    locations=client.venues.search(params={'ll': ll, 'radius':radius, 'categoryId':location_type[type]})
    pharmacies={}
    for location in locations['venues']:
        pharmacies[count_pharmacies]={}
        pharmacies[count_pharmacies]["name"]=location["name"]
        pharmacies[count_pharmacies]["location"]=location["location"]
        pharmacies[count_pharmacies]["distance"]=int(location["location"]["distance"])
        pharmacies[count_pharmacies]["address"]=location["location"]["formattedAddress"]
        count_pharmacies+=1
    pharmacies = sorted(pharmacies.items(), key = lambda x: x[1]['distance'])

    count_medical_centers=0
    locations=client.venues.search(params={'ll': ll, 'radius':radius, 'categoryId':location_type["medical_centers"]})
    medical_centers={}
    for location in locations['venues']:
        medical_centers[count_medical_centers]={}
        medical_centers[count_medical_centers]["name"]=location["name"]
        medical_centers[count_medical_centers]["location"]=location["location"]
        medical_centers[count_medical_centers]["distance"]=int(location["location"]["distance"])
        medical_centers[count_medical_centers]["address"]=location["location"]["formattedAddress"]
        count_medical_centers+=1
    medical_centers = sorted(medical_centers.items(), key = lambda x: x[1]['distance'])

    return render(request,"location_module/ajax/return_locations_pharmacies.html",{"total":len(medical_centers)+len(pharmacies),"radius":radius,"pharmacies":pharmacies[:5],"medical_centers":medical_centers[:5],"count_pharmacies":count_pharmacies,"count_medical_centers":count_medical_centers})

def get_address(request):
    lat =  str(round(float(request.GET.get('latitude')),6))
    long =  str(round(float(request.GET.get('longitude')),6))
    url="https://revgeocode.search.hereapi.com/v1/revgeocode?at={LAT}%2C{LNG}&apiKey={API_KEY}&lang=en".format(LAT=lat,LNG=long,API_KEY=settings.GEO_API_KEY)
    res=json.loads(requests.get(url).text)
    arr={}
    try:
        location=res["items"][0]["address"]
    except:
        return render(request,"location_module/ajax/get_address.html",{"address":"Not FOund"})

    arr["label"]=location["label"]
    arr["county"]=location["county"]
    arr["city"]=location["city"]
    arr["postalCode"]=location["postalCode"]

    return render(request,"location_module/ajax/get_address.html",{"address":arr})
