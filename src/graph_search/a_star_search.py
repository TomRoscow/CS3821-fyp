import heapq
import inspect

def manhattan_distance(p1, p2):
    """Calculate the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def heuristic_nearest_location(current, locations):
    """Estimate distance to the nearest unvisited location. Return 0 if all locations have been visited."""
    if not locations:  # If locations set is empty, all locations have been visited
        return 0
    return min(manhattan_distance(current, location) for location in locations)

def heuristic_sum_locations(current, locations):
    """Sum of Manhattan distances to all unvisited locations."""
    return sum(manhattan_distance(current, location) for location in locations)

def custom_heuristic(current, locations, N):
    """
    A custom heuristic function that estimates the cost to visit all unvisited locations.
    It calculates the Manhattan distance to the nearest unvisited location and adds an estimated
    minimal additional distance to cover all other unvisited locations.
    """
    if not locations:  # If locations set is empty, all locations have been visited
        return 0
    
    # Calculate Manhattan distances from the current position to each unvisited location
    distances = [manhattan_distance(current, location) for location in locations]
    
    # Find the nearest location to the current position
    nearest_location_distance = min(distances)
    
    # Estimate the additional distance needed after reaching the nearest location
    # This is a simplified estimation that could be replaced with a more sophisticated approach
    # Acknowledges that in a perfect scenario, each location is not too far from the others. This might be tougher in very large mazes
    estimated_additional_distance = (len(locations) - 1) * min(N - 1, nearest_location_distance)
    
    return nearest_location_distance + estimated_additional_distance

def heuristic_wrapper(heuristic, N=None):
    """A wrapper function that adapts the heuristic call based on its signature."""
    sig = inspect.signature(heuristic)
    if 'N' in sig.parameters:
        return lambda current, locations: heuristic(current, locations, N)
    else:
        return heuristic

def a_star_search(graph, start, N, heuristic, locations):
    """A* search to find the shortest path that touches all locations."""
    visited_locations = set([start]) if start in locations else set()
    # Wrap the heuristic with the wrapper function
    heuristic_call = heuristic_wrapper(heuristic, N)
    frontier = [(0 + heuristic_call(start, locations - visited_locations), 0, start, [start], visited_locations)]
    heapq.heapify(frontier)
    
    while frontier:
        _, cost, current, path, visited_locations = heapq.heappop(frontier)
        if visited_locations == locations:
            return path, cost  # Return path and cost when all locations are visited
        
        for next_node, next_cost in graph[current].items():
            if next_node in path:  # Avoid cycles, not just already visited locations
                continue
            
            new_cost = cost + next_cost
            new_path = path + [next_node]
            new_visited_locations = visited_locations | ({next_node} if next_node in locations else set())
            heapq.heappush(frontier, (new_cost + heuristic_call(next_node, locations - new_visited_locations), new_cost, next_node, new_path, new_visited_locations))
    
    return None, float('inf')  # Return None if no path found
