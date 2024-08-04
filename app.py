# app.py
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import random

app = Flask(__name__)

# Graph representation
graph = defaultdict(list)

# Default ACO parameters
DEFAULT_NUM_ANTS = 10
DEFAULT_NUM_ITERATIONS = 50
DEFAULT_ALPHA = 1  # pheromone importance
DEFAULT_BETA = 2   # distance importance
DEFAULT_RHO = 0.1  # pheromone evaporation rate
DEFAULT_Q = 1      # pheromone deposit factor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_edge', methods=['POST'])
def add_edge():
    data = request.json
    start = data['start']
    end = data['end']
    weight = data['weight']
    graph[start].append((end, weight))
    graph[end].append((start, weight))  # Assuming undirected graph
    return jsonify({"status": "success"})

@app.route('/reset', methods=['POST'])
def reset():
    global graph
    graph = defaultdict(list)
    return jsonify({"status": "success"})

@app.route('/generate_random_graph', methods=['POST'])
def generate_random_graph():
    global graph
    graph = defaultdict(list)
    data = request.json
    num_nodes = data['numNodes']
    num_edges = data['numEdges']
    
    nodes = [chr(65 + i) for i in range(min(num_nodes, 26))]  # A to Z
    
    for _ in range(num_edges):
        start = random.choice(nodes)
        end = random.choice([n for n in nodes if n != start])
        weight = random.randint(1, 10)
        graph[start].append((end, weight))
        graph[end].append((start, weight))
    
    return jsonify({"status": "success", "graph": dict(graph)})

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.json
    start = data['start']
    end = data['end']
    num_ants = int(data.get('numAnts', DEFAULT_NUM_ANTS))
    num_iterations = int(data.get('numIterations', DEFAULT_NUM_ITERATIONS))
    alpha = float(data.get('alpha', DEFAULT_ALPHA))
    beta = float(data.get('beta', DEFAULT_BETA))
    rho = float(data.get('rho', DEFAULT_RHO))
    q = float(data.get('q', DEFAULT_Q))
    
    path = ant_colony_optimization(graph, start, end, num_ants, num_iterations, alpha, beta, rho, q)
    return jsonify({"path": path})

def ant_colony_optimization(graph, start, end, num_ants, num_iterations, alpha, beta, rho, q):
    pheromones = defaultdict(lambda: defaultdict(lambda: 1.0))
    best_path = None
    best_path_length = float('inf')

    for _ in range(num_iterations):
        ant_paths = []
        for _ in range(num_ants):
            path = construct_solution(graph, pheromones, start, end, alpha, beta)
            if path:
                ant_paths.append(path)
                path_length = calculate_path_length(graph, path)
                if path_length < best_path_length:
                    best_path = path
                    best_path_length = path_length

        update_pheromones(graph, pheromones, ant_paths, rho, q)

    return best_path if best_path else []

def construct_solution(graph, pheromones, start, end, alpha, beta):
    current = start
    path = [current]
    visited = set([current])

    while current != end:
        next_node = select_next(graph, pheromones, current, visited, alpha, beta)
        if next_node is None:
            return None
        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path

def select_next(graph, pheromones, current, visited, alpha, beta):
    unvisited = [node for node, _ in graph[current] if node not in visited]
    if not unvisited:
        return None

    probabilities = []
    for node in unvisited:
        pheromone = pheromones[current][node]
        distance = next(weight for n, weight in graph[current] if n == node)
        probability = (pheromone ** alpha) * ((1.0 / distance) ** beta)
        probabilities.append(probability)

    total = sum(probabilities)
    normalized_probabilities = [p / total for p in probabilities]

    return random.choices(unvisited, weights=normalized_probabilities)[0]

def calculate_path_length(graph, path):
    return sum(next(weight for n, weight in graph[a] if n == b)
               for a, b in zip(path, path[1:]))

def update_pheromones(graph, pheromones, ant_paths, rho, q):
    # Evaporation
    for i in pheromones:
        for j in pheromones[i]:
            pheromones[i][j] *= (1 - rho)

    # Deposit
    for path in ant_paths:
        path_length = calculate_path_length(graph, path)
        for a, b in zip(path, path[1:]):
            pheromones[a][b] += q / path_length
            pheromones[b][a] += q / path_length

if __name__ == '__main__':
    app.run(debug=True)