import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "414d1c88-9d1c-4939-9d0c-6f9390717b3c"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0]["country"] if "country" in json_data["hits"][0] else ""
        state = json_data["hits"][0]["state"] if "state" in json_data["hits"][0] else ""

        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif state:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehículo de la lista anterior: ")

    if vehicle == "salir" or vehicle == "s":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de car.")

    loc1 = input("Ubicación inicial: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)
    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)
    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp # Se agrega 'locale=es' para obtener instrucciones en español
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Estado de la API de rutas: " + str(paths_status) + "\nURL de la API de rutas:\n" + paths_url)
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
        print("=================================================")

        if paths_status == 200:
            km = round(paths_data["paths"][0]["distance"] / 1000, 2)
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {:.2f} km".format(km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"] # Instrucciones en español
                distance = round(paths_data["paths"][0]["instructions"][each]["distance"] / 1000, 2)
                print("{0} ({1:.2f} km)".format(path, distance))
            print("=============================================")

        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")
