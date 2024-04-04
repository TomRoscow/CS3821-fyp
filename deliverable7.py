import argparse

from src.graph import create_maze_graph
from src.graph_search.minimax import GameState, minimax
from src.items import add_items
from src.monsters import static_monsters
from src.visualisation import draw_maze, update_character


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Size Selector")
    parser.add_argument("--size", type=str, choices=['small', 'medium', 'large'], help="Size of the maze: small, medium, or large")
    parser.add_argument("--verbose", type=bool, choices=[True, False])
    args = parser.parse_args()
    # Map the size choices to numerical sizes
    size_mapping = {
        'small': 4,
        'medium': 8,
        'large': 16
    }
    # Get the numerical size from the user's input
    size = size_mapping.get(args.size, 4)  # Default to 'small' (4x4) if not specified

    # Set up the maze with items on all tiles and some monsters
    flattened_exits, graph = create_maze_graph(size, seed=0)
    items_starts = add_items(size)
    graph, monsters_starts = static_monsters(graph, size)
    tile_exits, axs = draw_maze(flattened_exits, monsters_starts, items_starts, block=True)    

    num_items_from_start = len(items_starts)
    labyrinth = GameState((size-1, 0), monsters_starts, items_starts, num_items_from_start, graph)

    args.verbose = True
    game_over = False
    while not game_over:
        # Player's turn
        _, best_move = minimax(labyrinth, 3, True, args.verbose)
        erase_previous_position = labyrinth.player_position
        if best_move:
            labyrinth.player_position = best_move.player_position
        if labyrinth.player_position in labyrinth.item_locations:
            labyrinth.item_locations.remove(labyrinth.player_position)
        update_character(tile_exits, labyrinth.player_position, axs, "knight.png", erase_previous_position)
        
        # Check game over conditions after player's move
        if labyrinth.is_game_over():
            game_over = True
            if labyrinth.player_caught():
                print("Game over! Player was caught by monster and lost!")
            else:
                print("Game over! Player collected all items and won!")
            break

        # Monsters' turn
        for i, monster_position in enumerate(labyrinth.monster_positions):
            _, best_move_for_monster = minimax(labyrinth, 3, False, args.verbose)
            erase_previous_position = monster_position
            labyrinth.monster_positions[i] = best_move_for_monster.monster_positions[i]
            update_character(tile_exits, labyrinth.monster_positions[i], axs, "goblin.png", erase_previous_position)
            
            # Check game over condition after each monster's move
            if labyrinth.player_caught():
                game_over = True
                print("Game over! Player was caught by monster and lost!")
                break
