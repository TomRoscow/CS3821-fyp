# REFLEX AGENT AND MOVING MONSTERS (A* SEARCH WITH PATH REUSE)

import argparse

from a_star_search import a_star_search, adjust_path, heuristic_nearest_location
from graph import create_maze_graph
from greedy import greedy_search
from items import add_items
from monsters import static_monsters
from visualisation import draw_maze, update_character

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Size Selector")
    parser.add_argument("--size", type=str, choices=['small', 'medium', 'large'], help="Size of the maze: small, medium, or large")
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
    items_locations = add_items(size)
    graph, monsters_starts = static_monsters(graph, size)
    tile_exits, axs = draw_maze(flattened_exits, monsters_starts, items_locations, block=True)
    
    # Hero: plan path to collect all items using greedy search
    items_path_greedy = greedy_search(graph, (size-1, 0), items_locations, heuristic_nearest_location)
    if not items_path_greedy:
        raise Exception("No path found from character to all rewards with greedy search.")

    # Monsters: plan path for each monster to the main player's starting position using A* search
    monsters_with_paths = {}
    for i, start in enumerate(monsters_starts):
        path, _ = a_star_search(graph, start, size, heuristic_nearest_location, set([(size-1, 0)]))
        monsters_with_paths[i] = (start, path)
        if None in monsters_with_paths[i]:
            raise Exception("Unable to find path from monster to hero.")
        
    # Play the game
    hero_steps_taken = 0
    path_index = 1
    game_over = False
    hero_current_position = (size-1, 0)
    remaining_items_locations = set(items_locations)

    while not game_over:
    
        # Checks the hero isn't about to walk into a monster. If it is, it recalculates Draws the hero's next step
        hero_next_position = items_path_greedy[path_index]
        detour = False
        for monster, (monster_current_position, path) in monsters_with_paths.items():
            if monster_current_position == hero_next_position:
                detour = True
                break
        if detour:
            # Recalculate greedy path, removing the edge that leads to the monster
            adjusted_graph = graph.copy()
            del adjusted_graph[hero_current_position][monster_current_position]
            items_path_greedy = greedy_search(adjusted_graph, (size-1, 0), remaining_items_locations, heuristic_nearest_location)
            path_index = 1
            hero_next_position = items_path_greedy[path_index]

        # Draw the hero's next step, and check if it has won the game
        update_character(tile_exits, hero_next_position, axs, "knight.png", hero_current_position)
        path_index += 1
        hero_steps_taken += 1
        hero_current_position = hero_next_position
        remaining_items_locations.discard(hero_next_position)
        if len(remaining_items_locations) == 0:
            game_over = True
            print(f"Hero has collected all the items!")
            break

        # Let monsters react to the hero's move, and draw their next step. Then check if a monster has caught the hero
        for monster, (monster_current_position, path) in monsters_with_paths.items():
            new_path = adjust_path(graph, path, hero_current_position, size, heuristic_nearest_location)
            new_path = new_path[1:]
            monsters_with_paths[monster] = (path[1], new_path)
            print(f"Monster number: {monster}, location: {path[1]}")
            update_character(tile_exits, path[1], axs, "goblin.png", monster_current_position)
            if path[1] == hero_current_position:
                game_over = True
                print(f"Hero has been caught by a monster!")
                break

    print(f"Greedy shortest path collecting items from every tile: hero collected {len(remaining_items_locations)} in {hero_steps_taken} steps")