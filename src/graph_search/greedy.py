from src.graph_search.a_star_search import LimitedPriorityQueue

def greedy_search(graph, start, locations, heuristic):
    locations = set(locations)  # Convert the list of locations into a set for efficient lookup
    visited_locations = set([start]) if start in locations else set()
    initial_frontier = [heuristic(start, locations - visited_locations), start, [start], visited_locations, set([start])]
    frontier = LimitedPriorityQueue(limit=500)
    frontier.push(initial_frontier)

    while frontier:
        _, current, path_list, visited_locations, path_set = frontier.pop()
        if visited_locations == locations:
            return path_list  # Return path when all locations are visited

        for next_node, _ in graph[current].items():
            if path_list.count(next_node) > 3:  # Allow to visit a node twice but no more to avoid cycles
                continue  # Skip the next node

            new_visited_locations = visited_locations | ({next_node} if next_node in locations else set())
            new_path_list = path_list + [next_node]
            new_path_set = path_set | {next_node}
            new_frontier = heuristic(next_node, locations - new_visited_locations), next_node, new_path_list, new_visited_locations, new_path_set
            frontier.push(new_frontier)

    return None  # Return None if no path found that visits all locations
