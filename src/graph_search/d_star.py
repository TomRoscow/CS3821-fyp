import heapq

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = float('inf')
        self.rhs = float('inf')
        self.key = (float('inf'), float('inf'))

    def __lt__(self, other):
        return self.key < other.key
    
    # New method to find neighbours
    def get_neighbours(self, grid_size):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        neighbours = []
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1]:
                neighbours.append(Node(nx, ny))
        return neighbours

def calculate_key(node, start, km):
    return (min(node.cost, node.rhs) + h(node, start) + km, min(node.cost, node.rhs))

def h(node1, node2):
    # Using Manhattan distance as heuristic
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def initialise_search(graph, goal):
    goal.rhs = 0
    goal.key = calculate_key(goal, goal, 0)
    return [goal.key], {goal.key: goal}  # Priority queue with only the goal

def update_vertex(node, goal, open_list, open_dict, km):
    if node.cost != node.rhs:
        node.key = calculate_key(node, goal, km)
        heapq.heappush(open_list, node.key)
        open_dict[node.key] = node
    else:
        if node.key in open_dict:
            del open_dict[node.key]

def d_star_shortest_path(start, goal, open_list, open_dict, km, grid_size):
    while open_list and (open_list[0] < calculate_key(start, goal, km) or start.rhs > start.cost):
        k_old = heapq.heappop(open_list)
        node = open_dict.pop(k_old)
        if k_old < calculate_key(node, goal, km):
            heapq.heappush(open_list, calculate_key(node, goal, km))
            open_dict[calculate_key(node, goal, km)] = node
        elif node.cost > node.rhs:
            node.cost = node.rhs
            for neighbour in node.get_neighbours(grid_size):
                update_vertex(neighbour, goal, open_list, open_dict, km)
        else:
            node.cost = float('inf')
            update_vertex(node, goal, open_list, open_dict, km)
            for neighbour in node.get_neighbours(grid_size):
                update_vertex(neighbour, goal, open_list, open_dict, km)
