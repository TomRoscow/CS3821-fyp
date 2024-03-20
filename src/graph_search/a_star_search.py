import heapq
import inspect

def manhattan_distance(p1, p2):
    """Calculate the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def heuristic_nearest_corner(current, corners):
    """Estimate distance to the nearest unvisited corner. Return 0 if all corners have been visited."""
    if not corners:  # If corners set is empty, all corners have been visited
        return 0
    return min(manhattan_distance(current, corner) for corner in corners)

def heuristic_sum_corners(current, corners):
    """Sum of Manhattan distances to all unvisited corners."""
    return sum(manhattan_distance(current, corner) for corner in corners)

def custom_heuristic(current, corners, N):
    """
    A custom heuristic function that estimates the cost to visit all unvisited corners.
    It calculates the Manhattan distance to the nearest unvisited corner and adds an estimated
    minimal additional distance to cover all other unvisited corners.
    """
    if not corners:  # If corners set is empty, all corners have been visited
        return 0
    
    # Calculate Manhattan distances from the current position to each unvisited corner
    distances = [manhattan_distance(current, corner) for corner in corners]
    
    # Find the nearest corner to the current position
    nearest_corner_distance = min(distances)
    
    # Estimate the additional distance needed after reaching the nearest corner
    # This is a simplified estimation that could be replaced with a more sophisticated approach
    # Acknowledges that in a perfect scenario, each corner is not too far from the others. This might be tougher in very large mazes
    estimated_additional_distance = (len(corners) - 1) * min(N - 1, nearest_corner_distance)
    
    return nearest_corner_distance + estimated_additional_distance

def heuristic_wrapper(heuristic, N=None):
    """A wrapper function that adapts the heuristic call based on its signature."""
    sig = inspect.signature(heuristic)
    if 'N' in sig.parameters:
        return lambda current, corners: heuristic(current, corners, N)
    else:
        return heuristic

def get_corners(N):
    """Get all corners for an NxN maze."""
    return [(0, 0), (0, N-1), (N-1, 0), (N-1, N-1)]

def a_star_search(graph, start, N, heuristic):
    """A* search to find the shortest path that touches all corners."""
    corners = set(get_corners(N))
    visited_corners = set([start]) if start in corners else set()
    # Wrap the heuristic with the wrapper function
    heuristic_call = heuristic_wrapper(heuristic, N)
    frontier = [(0 + heuristic_call(start, corners - visited_corners), 0, start, [start], visited_corners)]
    heapq.heapify(frontier)
    
    while frontier:
        _, cost, current, path, visited_corners = heapq.heappop(frontier)
        if visited_corners == corners:
            return path, cost  # Return path and cost when all corners are visited
        
        for next_node, next_cost in graph[current].items():
            if next_node in path:  # Avoid cycles, not just already visited corners
                continue
            
            new_cost = cost + next_cost
            new_path = path + [next_node]
            new_visited_corners = visited_corners | ({next_node} if next_node in corners else set())
            heapq.heappush(frontier, (new_cost + heuristic_call(next_node, corners - new_visited_corners), new_cost, next_node, new_path, new_visited_corners))
    
    return None, float('inf')  # Return None if no path found
