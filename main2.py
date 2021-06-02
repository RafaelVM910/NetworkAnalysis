import warnings
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import json

warnings.filterwarnings('ignore')

g = nx.Graph()
nodes = 100000
edges = nodes * 5
infectar = round(nodes * 0.05)
weeks = 52

Sx = []
Ix = []
Rx = []
Mx = []
graphY = []

# States: 0 = S, 1 = I, 2 = R, 3 = M
# Colors: b = S, r = I, g = R, w = M

for i in range(nodes):
    g.add_node(i, state=0, days=0)

for i in range(edges):
    x = random.randint(0, nodes-1)
    y = random.randint(0, nodes-1)

    if x == y:
        y += random.randint(1, nodes - 2)
        if y >= nodes:
            y -= nodes-1

    g.add_edge(x, y)

for i in range(nodes):
    if len(g[i]) == 0:
        g.add_edge(i, (i + random.randint(1, nodes - 1)) % edges)
        edges += 1

for i in range(infectar):
    g.nodes[random.randint(0, nodes-1)]['state'] = 1

for days in range(weeks * 7):
    # Guardar informacion
    susceptibles = 0
    infectados = 0
    recuperados = 0
    muertos = 0

    for i in range(nodes):
        if g.nodes(data='state')[i] == 0:
            susceptibles += 1
        elif g.nodes(data='state')[i] == 1:
            infectados += 1
        elif g.nodes(data='state')[i] == 2:
            recuperados += 1
        elif g.nodes(data='state')[i] == 3:
            muertos += 1

    Sx.append(susceptibles)
    Ix.append(infectados)
    Rx.append(recuperados)
    Mx.append(muertos)
    graphY.append(days)

    # Invulnerabilizar
    for i in range(nodes):
        if g.nodes(data='state')[i] == 2 and g.nodes[i]['days'] == 7:
            g.nodes[i]['state'] = 0
            g.nodes[i]['days'] = 0

    # Infectar
    for i in range(nodes):
        if g.nodes(data='state')[i] == 1:
            for j in list(g.edges):
                if j[0] == i and g.nodes(data='state')[j[1]] == 0:
                    if random.randint(0, 100) < 60:
                        g.nodes[j[1]]['state'] = 1
                        g.nodes[i]['days'] = 0

            x = random.randint(0, 100)
            if 2 < x <= 10:
                g.nodes[i]['state'] = 2
                g.nodes[i]['days'] = 0

            elif x < 2:
                g.nodes[i]['state'] = 3
                g.nodes[i]['days'] = 0

            if g.nodes(data='days')[i] == 14:
                g.nodes[i]['state'] = 3
                g.nodes[i]['days'] = 0

    # Para aumentar los dias
    for i in range(nodes-1):
        g.nodes[i]['days'] += 1


# Grafo simulacion
pos = nx.spring_layout(g)
for i in range(nodes):
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 0], node_color='b', node_size=7)
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 1], node_color='r', node_size=7)
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 2], node_color='g', node_size=7)
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 3], node_color='grey', node_size=7)
nx.draw_networkx_edges(g, pos, width=0.2, alpha=0.5, edge_color='k')
plt.show()

# Grafica Personas
plt.plot(graphY, Sx, color='b', label='Susceptibles')
plt.plot(graphY, Ix, color='r', label='Infectados')
plt.plot(graphY, Rx, color='g', label='Recuperados')
plt.plot(graphY, Mx, color='k', label='Muertos')
plt.xlabel('Dias')
plt.ylabel('Personas')
plt.title('Estados a traves del tiempo')
plt.legend()
plt.show()


with open('Data.txt', 'a') as file:
    for i in range(len(Sx)):
        save = {"dia": i, "susceptibles": Sx[i], "infectados": Ix[i], "recuperados": Rx[i], "muertos": Mx[i]}
        json.dump(save, file, indent=4)
    file.close()
