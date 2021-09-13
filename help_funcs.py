from geopy.geocoders import Nominatim
from geopy import distance as geo_distance
from distance_model import Distance

""" 
This function get a strings source and destination,
and return from external service distance between them. (by geocoders)
"""
def get_geocoder_dis(src, dest):
    geocoder = Nominatim(user_agent='meir')
    cor1 = geocoder.geocode(src)
    cor2 = geocoder.geocode(dest)
    if not cor1:  # source not found in external service return -1
        return -1
    if not cor2:  # destination not found in external service return -2
        return -2
    lat1, long1 = cor1.latitude, cor1.longitude
    lat2, long2 = cor2.latitude, cor2.longitude
    place1 = (lat1, long1)
    place2 = (lat2, long2)
    float_dist = geo_distance.distance(place1, place2).km
    return float_dist


""" 
This function get a distance from local data base if the distance exist,
or find the distance in external service by get_geocoder_dis function 
and create new one and save him into the data base.
"""
def get_or_create_distance(source, destination):
    # Find the object
    dis = Distance.objects(source=source, destination=destination).first()
    # Check the opposite direction
    if not dis:
        dis = Distance.objects(source=destination, destination=source).first()
    # Local database not existed
    if not dis:
        # Get the distance from external service
        print("external service")
        geo_dis = get_geocoder_dis(source, destination)
        if geo_dis < 0:  # Not found
            return geo_dis
        dis = Distance(source=source, destination=destination, distance_in_km=geo_dis)
    # Update hits counter
    dis.hits += 1
    # Save it in local database
    dis.save()
    return dis.distance_in_km


# Get string name and returned cleaned name
def get_clean_name(name):
    name = name.lower()
    name = name.replace('-', ' ')
    return name


def create_distance_if_not_exist(source, destination, dist):
    # Checking if object exist in the data base
    dis = Distance.objects(source=destination, destination=source).first()  # opposite path
    if dis:
        return dis
    dis = Distance.objects(source=source, destination=destination).first()
    if dis:
        return dis
    # Create new one and save it into the data base
    dis = Distance(source=source, destination=destination, distance_in_km=dist)
    dis.save()
    return dis
