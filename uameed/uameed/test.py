# Sample run of TSP

from tsp import (
    run_tsp_on_simulator,
    sample_graph_with_weights,
    run_tsp_on_hardware,
    add_missing_edges,
)


graph = sample_graph_with_weights()

graph = add_missing_edges(graph)
z, result = run_tsp_on_simulator(graph)

# Sample run of TSP on hardware
z, result = run_tsp_on_hardware(graph)
