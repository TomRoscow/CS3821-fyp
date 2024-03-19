import random


def add_exits(tile_exits, row, col, potential_exits, exit_probability, N, graph):
    # Add exits and costs randomly but also check for neighbouring tiles
    current_exits = tile_exits[row][col]  #This just finds the tile you're targeting from the loop
    cost_function = lambda: random.randint(1, 10)
    if 'south' in potential_exits and row > 0 and 'north' in tile_exits[row - 1][col]:
        if random.random() < exit_probability:
            cost = cost_function()
            current_exits['north'] = cost
            graph = add_edge(graph, (row, col), (row - 1, col), cost)
    if 'north' in potential_exits and row < N - 1 and 'south' in tile_exits[row + 1][col]:
        if random.random() < exit_probability:
            cost = cost_function()
            current_exits['south'] = cost
            graph = add_edge(graph, (row, col), (row + 1, col), cost)
    if 'east' in potential_exits and col > 0 and 'west' in tile_exits[row][col - 1]:
        if random.random() < exit_probability:
            cost = cost_function()
            current_exits['west'] = cost
            graph = add_edge(graph, (row, col), (row, col - 1), cost)
    if 'west' in potential_exits and col < N - 1 and 'east' in tile_exits[row][col + 1]:
        if random.random() < exit_probability:
            cost = cost_function()
            current_exits['east'] = cost
            graph = add_edge(graph, (row, col), (row, col + 1), cost)
    return current_exits, graph
    #returns dictionary of direction:cost, and the graph with a costed directional edge added

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

def dead_end_handling(allow_dead_ends, current_exits, potential_exits):
    # Ensure at least two exits per block
    if allow_dead_ends:
        min_exits = 1
    else:
        min_exits = 2

    cost_function = lambda: random.randint(1, 10)
    #Also finding cost here since below we might be adding exits

    while len(current_exits) < min_exits:
        additional_exit = random.choice(list(potential_exits - set(current_exits.keys())))
        current_exits[additional_exit] = cost_function()
    return current_exits

def update_neighbouring_tiles(exit_direction, tile_exits, graph, row, col, N):
    cost_function = lambda: random.randint(1, 10)
    # Update neighbouring tiles
    if exit_direction == 'north' and row > 0:
        cost = cost_function()
        tile_exits[row - 1][col]['south'] = cost
        graph = add_edge(graph, (row - 1, col), (row, col), cost)
    if exit_direction == 'south' and row < N - 1:
        cost = cost_function()
        tile_exits[row + 1][col]['north'] = cost
        graph = add_edge(graph, (row + 1, col), (row, col), cost)
    if exit_direction == 'west' and col > 0:
        cost = cost_function()
        tile_exits[row][col - 1]['east'] = cost
        graph = add_edge(graph, (row, col - 1), (row, col), cost)
    if exit_direction == 'east' and col < N - 1:
        cost = cost_function()
        tile_exits[row][col + 1]['west'] = cost
        graph = add_edge(graph, (row, col + 1), (row, col), cost)
    return tile_exits

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

    if seed:
        random.seed(seed)

    # Initialise the graph as an empty dictionary. It will be populated with nested dictionaries
    # There will be costs for each exit for both directions/orientations and the graph is directional with doubled-up edges
    graph = {}

    # Generate exits for each tile
    for row in range(N):
        for col in range(N):
            
            potential_exits = determine_potential_exits(row, col, N)
            #what exits this tile could have given its location in the maze

            current_exits, graph = add_exits(tile_exits, row, col, potential_exits, exit_probability, N, graph)
            # current_exits is the tile as a dictionary of exit-direction:cost

            current_exits = dead_end_handling(allow_dead_ends, current_exits, potential_exits)

            for exit_direction in current_exits:
            # for every direction (key:value pair) in this tile's dictionary of exit directions and costs
                tile_exits = update_neighbouring_tiles(exit_direction, tile_exits, graph, row, col, N)

            
    # Flatten the exits list for compatibility with the drawing function
    # Where tile_exits is a dictionary (of the tile's exits) for the list of columns for the list of rows, flattened_exits is a flat list of the dictionaries. So one long list instead of a list of lists, ie a 2D array or square of elements.
    flattened_exits = [exit for row in tile_exits for exit in row]

    return flattened_exits, graph
