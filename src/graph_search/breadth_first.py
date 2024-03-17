def bfs(graph, start, goal):
    queue = [(start, [start])]  # Queue of (vertex, path) tuples
    visited = set()

    while queue:
        current, path = queue.pop(0)  # Dequeue the next vertex and path
        if current == goal:
            return path  # Return path to goal

        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None  # If goal not reachable
