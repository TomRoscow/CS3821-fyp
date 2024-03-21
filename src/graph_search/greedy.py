import heapq

def greedy_search(graph, start, locations, heuristic):
    locations = set(locations)  # Convert the list of locations into a set for efficient lookup
    visited_locations = set([start]) if start in locations else set()
    frontier = [(heuristic(start, locations - visited_locations), start, [start], visited_locations)]
    heapq.heapify(frontier)

    while frontier:
        _, current, path, visited_locations = heapq.heappop(frontier)
        if visited_locations == locations:
            return path  # Return path when all locations are visited

        for next_node, _ in graph[current].items():
            if next_node in path:
                continue  # Skip if the next node is already in the path to avoid cycles

            new_visited_locations = visited_locations | ({next_node} if next_node in locations else set())
            new_path = path + [next_node]
            heapq.heappush(frontier, (heuristic(next_node, locations - new_visited_locations), next_node, new_path, new_visited_locations))

    return None  # Return None if no path found that visits all locations
