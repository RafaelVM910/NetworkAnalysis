import warnings
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import json

warnings.filterwarnings('ignore')

g = nx.Graph()
nodes = 20
edges = nodes * 5
weeks = 4

# States: 0 = S, 1 = I, 2 = R, 3 = M

# Crear nodos
for i in range(nodes):
    g.add_node(i, state=0, days=0)

# Crear vertices
for i in range(edges):
    x = random.randint(0, nodes-1)
    y = random.randint(0, nodes-1)

    if x == y:
        y += random.randint(1, nodes - 2)
        if y >= nodes:
            y -= nodes-1

    g.add_edge(x, y)

# Asegurar vertices para todos
for i in range(nodes):
    if len(g[i]) == 0:
        g.add_edge(i, (i + random.randint(1, nodes - 1)) % edges)

# Infectar nodo
g.nodes[random.randint(0, nodes-1)]['state'] = 1

# Simulacion
for days in range(weeks * 7):
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
                    if random.randint(0, 100) < 50:
                        g.nodes[j[1]]['state'] = 1
                        g.nodes[j[1]]['days'] = 0

            x = random.randint(0, 100)
            if 2 < x <= 15:
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


# Dibujar grafo
pos = nx.spring_layout(g)
for i in range(nodes):
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 0], node_color='b')
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 1], node_color='r')
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 2], node_color='g')
    nx.draw_networkx_nodes(g, pos, [x for x in g.nodes() if g.nodes(data='state')[x] == 3], node_color='grey')
nx.draw_networkx_edges(g, pos, width=1.0, alpha=0.5, edge_color='k')
plt.show()
