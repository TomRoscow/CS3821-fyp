import random
import heapq  # for priority queue

def uniform_cost_search(graph, start, goal):
    """
    Perform uniform-cost search from start to goal.
    graph: A dictionary representing the maze, where keys are node coordinates and values are sets of neighbouring node coordinates.
    start: Tuple representing the starting coordinates (row, col).
    goal: Tuple representing the goal coordinates (row, col).
    Returns the path from start to goal and its cost if a path exists, otherwise None.
    """
    frontier = [(0, start, [])]  # Priority queue: (cost, current_node, path)
    explored = set()  # Keep track of explored nodes

    while frontier:
        cost, current_node, path = heapq.heappop(frontier)
        
        if current_node in explored:
            continue

        # Add current node to the path
        path = path + [current_node]

        if current_node == goal:
            return path, cost  # Found the goal

        explored.add(current_node)

        for neighbour in graph[current_node]:
            if neighbour not in explored:
                # Calculate the cost to move to the neighbour
                # Assumes graph edges represent actual movement costs
                neighbour_cost = graph[current_node][neighbour]
                heapq.heappush(frontier, (cost + neighbour_cost, neighbour, path))

    return None, None  # No path found
