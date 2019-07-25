# coding: utf-8
# Made by Rafael Pontes

import json, math, requests

def dist_pontos(p1, p2):
    R = 6378.137 # Raio da Terra em km
    dist_latitudinal = p2[0] * math.pi / 180 - p1[0] * math.pi / 180
    dist_longitudinal = p2[1] * math.pi / 180 - p1[1] * math.pi / 180
    a = math.sin(dist_latitudinal/2) * math.sin(dist_latitudinal/2) + \
            math.cos(p1[0] * math.pi / 180) * math.cos(p2[0] * \
            math.pi / 180) * math.sin(dist_longitudinal/2) * math.sin(dist_longitudinal/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # Distancia em metros!

with open("bike.json", "r", encoding="utf-8") as bikes_json:
    
    bikes = json.load(bikes_json)
    bikes_headers = bikes["COLUMNS"]
    bikes = bikes["DATA"]

    url = "http://nominatim.openstreetmap.org/search"
    
    rua = input("Digite a rua: ")
    # rua = "Avenida Bartolomeu Mitre"

    params = {
        "street": rua,
        "city": "Rio de Janeiro",
        "format": "json",
        "polygon": 0,
        "addressdetails": 0
    }

    r = requests.get(url=url, params=params)

    r_json = r.json()
    if (len(r_json) == 0):
        print("Nenhuma rua encontrada com esse nome.")
    else:
        dados_rua = r.json()[0]
        print("===================================")
        print("Dados da rua solicitada:")
        print(f"Endereço: {dados_rua['display_name']}")
        print(f"Latidude: {dados_rua['lat']}")
        print(f"Longitude: {dados_rua['lon']}")
        print("===================================")

        ponto_rua = (float(dados_rua['lat']), float(dados_rua['lon']))
        pontos_bikes = [(float(b[-2]), float(b[-1])) for b in bikes]
        
        for b in range(len(bikes)):
            bikes[b].append(dist_pontos(ponto_rua, pontos_bikes[b]))
        
        bikes = [tuple(b) for b in bikes]
        bikes = sorted(bikes, key=lambda bikes: bikes[7])
        
        print("\n===================================")
        print("Lista de bicicletários ordenados da menor para a maior distância:")
        for b in bikes:
            print(
                f" * Estação: {b[1]}, local: {b[3]}, n. {b[4]} => Distância: {b[-1]:.2f} metros.")
        print("\n===================================")

input("\n\nPressione ENTER para fechar.")
