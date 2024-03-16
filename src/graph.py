import random


def create_maze_graph(N, allow_dead_ends=False, seed=None):
    exits_options = ['north', 'south', 'east', 'west']
    tile_exits = [[[] for _ in range(N)] for _ in range(N)]  # Initialize exits for NxN maze
    exit_probability = 0.25

    if seed:
        random.seed(seed)

    # Initialize the graph as an empty dictionary
    graph = {}

    # Helper function to add an edge in the graph
    def add_edge(node1, node2):
        if node1 in graph:
            graph[node1].add(node2)
        else:
            graph[node1] = {node2}
        if node2 in graph:
            graph[node2].add(node1)
        else:
            graph[node2] = {node1}
        # final four lines make node2's pathway match what node1 wants

    # Generate exits for each tile
    for row in range(N):
        for col in range(N):
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

            # Add exits randomly but also check for neighbouring tiles
            current_exits = tile_exits[row][col]
            if 'south' in potential_exits and row > 0 and 'north' in tile_exits[row - 1][col]:
                if random.random() < exit_probability:
                    current_exits.append('north')
            if 'north' in potential_exits and row < N - 1 and 'south' in tile_exits[row + 1][col]:
                if random.random() < exit_probability:
                    current_exits.append('south')
            if 'east' in potential_exits and col > 0 and 'west' in tile_exits[row][col - 1]:
                if random.random() < exit_probability:
                    current_exits.append('west')
            if 'west' in potential_exits and col < N - 1 and 'east' in tile_exits[row][col + 1]:
                if random.random() < exit_probability:
                    current_exits.append('east')

            # Ensure at least two exits per block
            if allow_dead_ends:
                min_exits = 1
            else:
                min_exits = 2
            while len(current_exits) < min_exits:
                additional_exit = random.choice(list(potential_exits - set(current_exits)))
                current_exits.append(additional_exit)

            # Update neighbouring tiles
            for exit_direction in current_exits:
                if exit_direction == 'north' and row > 0:
                    tile_exits[row - 1][col].append('south')
                    add_edge((row, col), (row - 1, col))
                if exit_direction == 'south' and row < N - 1:
                    tile_exits[row + 1][col].append('north')
                    add_edge((row, col), (row + 1, col))
                if exit_direction == 'west' and col > 0:
                    tile_exits[row][col - 1].append('east')
                    add_edge((row, col), (row, col - 1))
                if exit_direction == 'east' and col < N - 1:
                    tile_exits[row][col + 1].append('west')
                    add_edge((row, col), (row, col + 1))

    # Flatten the exits list for compatibility with the drawing function
    flattened_exits = [exit for row in tile_exits for exit in row]

    return flattened_exits, graph
