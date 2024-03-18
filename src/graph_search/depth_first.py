def dfs(graph, start, goal):
    stack = [(start, [start])]  # Stack of (vertex, path) tuples
    visited = set()

    while stack:
        current, path = stack.pop()  # Pop the most recent vertex and path

        if current not in visited:
            visited.add(current)

        if current == goal:
            return path  # Return path to goal

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None  # If goal not reachable
