import random


def determine_potential_exits(row, col, N):
    # Determine potential exits based on maze boundaries
    potential_exits = set()
    if row > 0:
        potential_exits.add('north')
    if row < N - 1:
        potential_exits.add('south')
    if col > 0:
        potential_exits.add('west')
    if col < N - 1:
        potential_exits.add('east')
    return potential_exits

def add_exits(allow_dead_ends, current_exits, potential_exits, graph, row, col):
    # Ensure at least two exits per block
    if allow_dead_ends:
        min_exits = 1
    else:
        min_exits = 2

    cost = 1

    while len(current_exits) < min_exits:
        additional_exit = random.choice(list(potential_exits - set(current_exits.keys())))
        current_exits[additional_exit] = cost
        if additional_exit == 'north':
            graph = add_edge(graph, (row, col), (row - 1, col), cost)
        if additional_exit == 'south':
            graph = add_edge(graph, (row, col), (row + 1, col), cost)
        if additional_exit == 'west':
            graph = add_edge(graph, (row, col), (row, col - 1), cost)
        if additional_exit == 'east':
            graph = add_edge(graph, (row, col), (row, col + 1), cost)
    return current_exits, graph

def update_neighbouring_tiles(exit_direction, tile_exits, graph, row, col, N):
    cost = 1
    # Update neighbouring tiles
    if exit_direction == 'north' and row > 0:
        tile_exits[row - 1][col]['south'] = cost
        graph = add_edge(graph, (row - 1, col), (row, col), cost)
    if exit_direction == 'south' and row < N - 1:
        tile_exits[row + 1][col]['north'] = cost
        graph = add_edge(graph, (row + 1, col), (row, col), cost)
    if exit_direction == 'west' and col > 0:
        tile_exits[row][col - 1]['east'] = cost
        graph = add_edge(graph, (row, col - 1), (row, col), cost)
    if exit_direction == 'east' and col < N - 1:
        tile_exits[row][col + 1]['west'] = cost
        graph = add_edge(graph, (row, col + 1), (row, col), cost)
    return graph, tile_exits

# This function adds a directed edge with a specified cost to the graph.
# The graph is represented as a dictionary where each key is a node, and its value is another dictionary mapping neighbouring nodes to the costs of the edges leading to them.
# If node1 already exists in the graph, it adds the edge to node2 with the new cost. If node1 isn't in the graph, it doesn't have any outgoing edges yet, so a new entry is created in the graph with node1 as the key and the value a dictionary with node2 as the key and the cost as the value.
# This function gets called by add_exits when a tile has an exit to a neighbour and generates its cost, and by update_neighbouring_tiles when the neighbour is made to reciprocate the exit and its own cost is generated.
def add_edge(graph, node1, node2, cost):
    if node1 in graph:
        graph[node1][node2] = cost
    else:
        graph[node1] = {node2: cost}
    return graph

def create_maze_graph(N, allow_dead_ends=False, seed=None):
    tile_exits = [[{} for _ in range(N)] for _ in range(N)]  # Initialise exits for NxN maze
    exit_probability = 0.25

    if seed is not None:
        random.seed(seed)

    # Initialise the graph as an empty dictionary. It will be populated with nested dictionaries
    # There will be costs for each exit for both directions/orientations and the graph is directional with doubled-up edges
    graph = {}

    # Generate exits for each tile
    for row in range(N):
        for col in range(N):
            
            potential_exits = determine_potential_exits(row, col, N)
            #what exits this tile could have given its location in the maze

            # current_exits is the tile as a dictionary of exit-direction:cost
            current_exits = tile_exits[row][col]
            current_exits, graph = add_exits(allow_dead_ends, current_exits, potential_exits, graph, row, col)

            for exit_direction in current_exits:
            # for every direction (key:value pair) in this tile's dictionary of exit directions and costs
                graph, tile_exits = update_neighbouring_tiles(exit_direction, tile_exits, graph, row, col, N)

            assert len(current_exits) == len(graph[(row, col)]), 'Tile exits do not match graph'
            assert len(current_exits) >= 1, 'Tile has no exits'
            if ~allow_dead_ends:
                assert len(current_exits) >= 2, 'Tile has a dead end'

            
    # Flatten the exits list for compatibility with the drawing function
    # Where tile_exits is a dictionary (of the tile's exits) for the list of columns for the list of rows, flattened_exits is a flat list of the dictionaries. So one long list instead of a list of lists, ie a 2D array or square of elements.
    flattened_exits = [exit for row in tile_exits for exit in row]

    return flattened_exits, graph
