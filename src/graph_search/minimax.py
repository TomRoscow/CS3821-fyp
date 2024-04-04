class GameState:
    def __init__(self, player_position, monster_positions, item_locations, num_items_from_start, graph):
        self.player_position = player_position
        self.monster_positions = monster_positions
        self.item_locations = item_locations
        self.num_items_from_start = num_items_from_start
        self.graph = graph

    def is_game_over(self):
        # Check for win/loss conditions
        return self.player_caught() or self.all_items_collected()

    def player_caught(self):
        return any(monster_pos == self.player_position for monster_pos in self.monster_positions)

    def all_items_collected(self):
        return len(self.item_locations) == 0
    
    def calculate_average_distance_from_monsters(self):
        if not self.monster_positions:
            return float('inf')  # Avoids division by zero; encourages moving towards items if no monsters are present

        total_distance = sum(self.manhattan_distance(self.player_position, monster_pos) for monster_pos in self.monster_positions)
        average_distance = total_distance / len(self.monster_positions)
        return average_distance
    
    @staticmethod
    def manhattan_distance(point_a, point_b):
        return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])
    
    def get_children(self, is_player, verbose):
        children = []
        potential_item_locations = self.item_locations.copy()  # Make copies to avoid modifying originals
        possible_next_positions = self.graph[self.player_position].keys()
        
        if is_player:
            # Player's turn
            for possible_next_position in possible_next_positions:
                new_monster_positions = self.monster_positions[:]
                if possible_next_position in potential_item_locations:
                    potential_item_locations.remove(possible_next_position)
                if verbose:
                    print(f"Evaluating state where player moves to {possible_next_position}...")
                child_state = GameState(possible_next_position, new_monster_positions, potential_item_locations, self.num_items_from_start, self.graph)
                children.append(child_state)
        else:
            # Monsters' turn
            for i, monster_position in enumerate(self.monster_positions):
                for possible_next_position in self.graph[monster_position].keys():
                    new_monster_positions = self.monster_positions[:]
                    new_monster_positions[i] = possible_next_position
                    if verbose:
                        print(f"Evaluating state where monster {i} moves to {possible_next_position}...")
                    child_state = GameState(self.player_position, new_monster_positions, potential_item_locations, self.num_items_from_start, self.graph)
                    children.append(child_state)
                    
        return children

    def evaluate(self, verbose):
        if self.player_caught():
            if verbose:
                print(f"Game over. Player has been caught by a monster and lost.")
            return float('-inf')  # Loss
        if self.all_items_collected():
            if verbose:
                print(f"Game over. Player has collected all items and won.")
            return float('inf')   # Win
        
        rewards_collected = self.num_items_from_start - len(self.item_locations)
        average_distance_from_all_monsters = self.calculate_average_distance_from_monsters()

        # Apply a graduated scale for proximity
        proximity_bonus = 0
        for monster_pos in self.monster_positions:
            distance = self.manhattan_distance(self.player_position, monster_pos)
            if distance == 1:
                proximity_bonus += 500

        score = rewards_collected * 100 - average_distance_from_all_monsters * 2 + proximity_bonus
        if verbose:
            print(f"State score: {score}")
        return score  # Bigger is better for player, smaller is better for monsters
    
def minimax(node, depth, is_maximising_player, verbose):
    if depth == 0 or node.is_game_over():
        return node.evaluate(verbose), node

    best_state = None

    if is_maximising_player:
        max_eval = float('-inf')
        best_state = None
        for child in node.get_children(True, verbose):
            eval, _ = minimax(child, depth - 1, False, verbose)
            if eval > max_eval:
                max_eval = eval
                best_state = child
        return max_eval, best_state
    else:
        min_eval = float('inf')
        best_state = None
        for child in node.get_children(False, verbose):
            eval, _ = minimax(child, depth - 1, True, verbose)
            if eval < min_eval:
                min_eval = eval
                best_state = child
        return min_eval, best_state
