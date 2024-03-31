import heapq
import inspect
import numpy as np

class LimitedPriorityQueue:
    def __init__(self, limit):
        self.heap = []
        self.limit = limit
    
    def push(self, item):
        if len(self.heap) < self.limit:
            heapq.heappush(self.heap, item)
        else:
            # Push item and pop the highest cost item if the heap is full
            heapq.heappushpop(self.heap, item)
    
    def pop(self):
        return heapq.heappop(self.heap)
    
    def __len__(self):
        return len(self.heap)

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
    initial_frontier = (0 + heuristic_call(start, set(locations) - visited_locations), 0, start, [start], visited_locations, set([start]))
    frontier = LimitedPriorityQueue(limit=1000)
    frontier.push(initial_frontier)
    
    while frontier:
        _, cost, current, path_list, visited_locations, path_set = frontier.pop()
        if visited_locations == set(locations):
            return path_list, cost  # Return path and cost when all locations are visited
        
        for next_node, next_cost in graph[current].items():
            if path_set.count(next_node) > 2:  # Allow to visit a node twice but no more to avoid cycles
                continue # Skip the next node
            
            new_cost = cost + next_cost
            new_path_list = path_list + [next_node]
            new_path_set = path_set | {next_node}
            new_visited_locations = visited_locations | ({next_node} if next_node in locations else set())
            new_frontier = (new_cost + heuristic_call(next_node, set(locations) - new_visited_locations), new_cost, next_node, new_path_list, new_visited_locations, new_path_set)
            frontier.push(new_frontier)
    
    return None, float('inf')  # Return None if no path found

def adjust_path(graph, path, new_end, size, heuristic):
    """Adjusts the given path to account for the new end position."""
    if new_end in path:
        # If the new end is already in the path, trim the path to that point
        return path[:path.index(new_end) + 1]
    else:
        # Find the closest point in the path to the new end and recalculate from there
        idx = np.argmin([manhattan_distance(point, new_end) for point in path])
        closest_point = path[idx]
        new_start_index = path.index(closest_point)
        new_path_part, _ = a_star_search(graph, closest_point, size, heuristic, [new_end])
        if new_path_part is not None:
            return path[:new_start_index] + new_path_part
        else:
            raise Exception("Unable to find path from monster to hero.")