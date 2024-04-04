# Effectiveness: path length
# Efficiency: easiest option is walltime because it doesn't require modifying existing functions. Other options include nodes visited, memory used...

import time
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

from src.graph_search.a_star_search import a_star_search, heuristic_nearest_location
from src.graph import create_maze_graph
from src.graph_search.greedy import greedy_search
from src.items import add_items
from src.monsters import static_monsters

def compare_a_star_greedy():
    n_runs = 20 # Should be 100 eventually
    results = pd.DataFrame()

    for algorithm_name, algorithm_function in [("A*", a_star_search), ("greedy", greedy_search)]:
        for maze_size, maze_dimension in [("small", 4), ("medium", 8), ("large", 16)]:
            print(f"Beginning {algorithm_name} search on {maze_size} maze")
            for i in tqdm(range(n_runs)): # This creates a progress bar so you can estimate how long it's going to take (probably a long time)
                # Set up maze graph, monsters, items
                _, graph = create_maze_graph(maze_dimension, False, i)
                graph, _ = static_monsters(graph, maze_dimension)
                items_locations = add_items(maze_dimension)
                start_time = time.time()
                if algorithm_name == "A*":
                    path, _ = algorithm_function(graph, (maze_dimension-1, 0), maze_dimension, heuristic_nearest_location, set(items_locations))
                elif algorithm_name == "greedy":
                    path = algorithm_function(graph, (maze_dimension-1, 0), items_locations, heuristic_nearest_location)
                end_time = time.time()
                if path:
                    found_path = True
                    path_length = len(path)
                else:
                    found_path = False
                    path_length = None
                res = pd.DataFrame({"algorithm": algorithm_name,
                                    "maze size": maze_size,
                                    "success": found_path,
                                    "path length": path_length,
                                    "time": end_time - start_time},
                                    index=[0])

                results = pd.concat([results, res])

    results = results.reset_index() # This is because seaborn complains if there are duplicate indices in the dataframe
    results.to_csv("../a_start_greedy_comparison_results.csv") # Save it to avoid running again because it takes a long time
    fig, ax = plt.subplots(1, 3)

    # Plot mean +- 95% confidence interval of effectiveness (rate of finding a path), over maze sizes (on the x-axis), separated by algorithm (separate lines/colours)
    sns.lineplot(data=results, x="maze size", y="success", hue="algorithm", errorbar="ci", ax=ax[0])

    # Plot mean +- standard error of effectiveness (path length), over maze sizes (on the x-axis), separated by algorithm (separate lines/colours)
    sns.lineplot(data=results, x="maze size", y="path length", hue="algorithm", errorbar="se", ax=ax[1])

    # Plot mean +- standard error of efficiency (time)
    sns.lineplot(data=results, x="maze size", y="time", hue="algorithm", errorbar="se", ax=ax[2])

    ax[0].set_title("Effectiveness (success rate)")
    ax[1].set_title("Effectiveness (path length)")
    ax[2].set_title("Efficiency")

    plt.tight_layout() # This makes sure there is a nice spacing between the subplots

    plt.show()