import random


def add_exits(tile_exits, row, col, potential_exits, exit_probability, N):
    # Add exits and costs randomly but also check for neighbouring tiles
    current_exits = tile_exits[row][col]  #This just finds the tile you're targeting from the loop
    cost_function = lambda: random.randint(1, 10)
    if 'south' in potential_exits and row > 0 and 'north' in tile_exits[row - 1][col]:
        if random.random() < exit_probability:
            current_exits['north'] = cost_function()
    if 'north' in potential_exits and row < N - 1 and 'south' in tile_exits[row + 1][col]:
        if random.random() < exit_probability:
            current_exits['south'] = cost_function()
    if 'east' in potential_exits and col > 0 and 'west' in tile_exits[row][col - 1]:
        if random.random() < exit_probability:
            current_exits['west'] = cost_function()
    if 'west' in potential_exits and col < N - 1 and 'east' in tile_exits[row][col + 1]:
        if random.random() < exit_probability:
            current_exits['east'] = cost_function()
    return current_exits

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
        tile_exits[row - 1][col]['south'] = cost_function()
        graph = add_edge(graph, (row, col), (row - 1, col))
    if exit_direction == 'south' and row < N - 1:
        tile_exits[row + 1][col]['north'] = cost_function()
        graph = add_edge(graph, (row, col), (row + 1, col))
    if exit_direction == 'west' and col > 0:
        tile_exits[row][col - 1]['east'] = cost_function()
        graph = add_edge(graph, (row, col), (row, col - 1))
    if exit_direction == 'east' and col < N - 1:
        tile_exits[row][col + 1]['west'] = cost_function()
        graph = add_edge(graph, (row, col), (row, col + 1))
    return tile_exits

# Helper function to add an edge in the graph
def add_edge(graph, node1, node2):
    if node1 in graph:
        graph[node1].add(node2)
    else:
        graph[node1] = {node2}
    if node2 in graph:
        graph[node2].add(node1)
    else:
        graph[node2] = {node1}
    # final four lines make node2's pathway match what node1 wants
    return graph

def create_maze_graph(N, allow_dead_ends=False, seed=None):
    tile_exits = [[{} for _ in range(N)] for _ in range(N)]  # Initialize exits for NxN maze
    exit_probability = 0.25

    if seed:
        random.seed(seed)

    # Initialize the graph as an empty dictionary
    graph = {}

    # Generate exits for each tile
    for row in range(N):
        for col in range(N):
            
            potential_exits = determine_potential_exits(row, col, N)
            #what exits this tile could have given its location in the maze

            current_exits = add_exits(tile_exits, row, col, potential_exits, exit_probability, N)
            # current_exits is the tile

            current_exits = dead_end_handling(allow_dead_ends, current_exits, potential_exits)

            for exit_direction in current_exits:
                tile_exits = update_neighbouring_tiles(exit_direction, tile_exits, graph, row, col, N)

            
    # Flatten the exits list for compatibility with the drawing function
    flattened_exits = [exit for row in tile_exits for exit in row]

    return flattened_exits, graph
