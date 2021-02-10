from geopy.distance import distance, geodesic, great_circle
import requests
import json


# sitios de prueba
poblado = (6.213416598717274, -75.57788098175646)
estrella = (6.1534935564101865, -75.62651764032978)

# Calculo de la distancia geodecica con geopy
def geodesic_dist(point1, point2):
    d = geodesic((point1[0], point1[1]), ((point2[0], point2[1]))).m
    return d

dist = geodesic_dist(poblado, estrella)
print("Geopy")
print(dist)

# Calculo de la distancia en carretera con OMS
def road_dis_OSM(point1, point2):
    # Nota que deben entrase las coordenadas en el orden longitud latitud
    r = requests.get(f"""http://router.project-osrm.org/route/v1/car/{point1[1]},{point1[0]};{point2[1]},{point2[0]}?overview=false""")
    routes = json.loads(r.content)
    route_1 = routes.get("routes")[0]
    distance = route_1["distance"]
    return distance

dist = road_dis_OSM(poblado, estrella)
print("Open Street Map")
print(dist)



API_KEY = "AIzaSyBrcChgM41NgYRy7FL4oXoxkz6KJbrKyJY" # Debes obtener tu propia clave
def road_dis_GM(point1, point2, API_KEY):
    # Deben convertirse las coordenadas a un string
    point1s = ",".join([str(point1[0]), str(point1[1])])
    point2s = ",".join([str(point2[0]), str(point2[1])])
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={point1s}&destination={point2s}&mode=driving&key={API_KEY}"
    r = requests.get(url)
    results = json.loads(r.content)
    legs = results.get("routes").pop(0).get("legs")
    return legs[0].get("distance")

dist = road_dis_GM(poblado, estrella, API_KEY)
print("GoogleMaps")
print("GoogleMaps" , str(dist))


