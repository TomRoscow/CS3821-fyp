# Effectiveness: path length
# Efficiency: easiest option is walltime because it doesn't require modifying existing functions. Other options include nodes visited, memory used...

import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.graph import create_maze_graph
from src.graph_search.a_star_search import a_star_search, heuristic_nearest_location
from src.graph_search.greedy import greedy_search
from src.items import add_items
from src.monsters import static_monsters
from tqdm import tqdm


def compare_a_star_greedy():
    n_runs = 50
    results = pd.DataFrame()
    for i in tqdm(range(n_runs)):
        tqdm.write(f"\nBeginning run {i} of {n_runs}...")
        for algorithm_name, algorithm_function in [("A*", a_star_search), ("greedy", greedy_search)]:
            for maze_size, maze_dimension in [("small", 4), ("medium", 8), ("large", 16)]:
                tqdm.write(f"  running {algorithm_name} search on {maze_size} maze")
                # Set up maze graph, monsters, items
                _, graph = create_maze_graph(maze_dimension, False, seed=i)
                graph, _ = static_monsters(graph, maze_dimension, seed=i)
                items_locations = add_items(maze_dimension)
                if len(items_locations)==0:
                    raise Exception("no items")
                start_time = time.time()
                if algorithm_name=="A*":
                    path, _= algorithm_function(graph, (maze_dimension-1, 0), maze_dimension, heuristic_nearest_location, set(items_locations))
                elif algorithm_name=="greedy":
                    path = algorithm_function(graph, (maze_dimension-1, 0), set(items_locations), heuristic_nearest_location)
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
                                    index=[i])
                results = pd.concat([results, res])

        results = results.reset_index(drop=True) # This is because seaborn complains if there are duplicate indices in the dataframe
        results.to_csv(f"./output/a_star_greedy_comparison_results_{i+1}_runs.csv") # Save it to avoid running again because it takes a long time

        fig, ax = plt.subplots(1, 3, figsize=(10, 3 ))

        # Plot mean +- 95% confidence interval of effectiveness (rate of finding a path), over maze sizes (on the x-axis), separated by algorithm (separate lines/colours)
        sns.lineplot(data=results, x="maze size", y="success", hue="algorithm", errorbar="ci", ax=ax[0])

        # Plot mean +- standard error of effectiveness (path length), over maze sizes (on the x-axis), separated by algorithm (separate lines/colours)
        sns.lineplot(data=results, x="maze size", y="path length", hue="algorithm", errorbar="se", ax=ax[1])

        # Plot mean +- standard error of efficiency (time)
        sns.lineplot(data=results, x="maze size", y="time", hue="algorithm", errorbar="se", ax=ax[2])

        ax[0].set_title("Effectiveness (success rate)")
        ax[1].set_title("Effectiveness (path length)")
        ax[2].set_title("Efficiency")
        ax[2].set_ylabel("time (seconds)")

        plt.tight_layout() # This makes sure there is a nice spacing between the subplots

        plt.show(block=False)
        plt.savefig(f"./output/a_star_greedy_comparison_results_{i+1}_runs.png")
