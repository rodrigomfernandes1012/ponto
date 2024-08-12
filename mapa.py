import osmnx as ox
import networkx as nx

# Define as localidades de origem e destino
origem = "Rua Marco Polo 308, São Paulo, Brasil"
destino = "Avenida Amador Bueno da Veiga 100, São Paulo, Brasil"

# Obtém o grafo de ruas da cidade
G = ox.graph_from_place("São Paulo, Brasil", network_type='drive')

# Obtém as coordenadas de origem e destino
origem_loc = ox.geocode(origem)
destino_loc = ox.geocode(destino)

# Encontra os nós mais próximos para as localidades
origem_node = ox.distance.nearest_nodes(G, origem_loc[1], origem_loc[0])
destino_node = ox.distance.nearest_nodes(G, destino_loc[1], destino_loc[0])

# Calcula a rota
rota = nx.shortest_path(G, origem_node, destino_node)

# Converte a rota em um GeoDataFrame para visualização
rota_geodata = ox.plot_route_folium(G, rota)

# Salva o mapa em um arquivo HTML
rota_geodata.save('rota.html')

# Exibe a rota
print("Rota calculada entre", origem, "e", destino)