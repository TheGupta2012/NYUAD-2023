"""
    This module contains fucntions to find the shortest hamiltonian path using qiskit

    This code is a part of Qiskit

    © Copyright IBM 2017, 2021.

    This code is licensed under the Apache License, Version 2.0. You may
    obtain a copy of this license in the LICENSE.txt file in the root directory
    of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

    Any modifications or derivative works of this code must retain this
    copyright notice, and modified files need to carry a notice indicating
    that they have been altered from the originals.

"""

from typing import Tuple, List, Optional, Union
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit_optimization.applications import Tsp
from qiskit.circuit.library import TwoLocal
from qiskit_optimization.applications import Tsp
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import SPSA
from qiskit.algorithms.minimum_eigensolvers import SamplingMinimumEigensolverResult
from qiskit.utils import algorithm_globals
from qiskit.primitives import Sampler
import networkx as nx
import numpy as np
from qiskit.algorithms.minimum_eigen_solvers import VQE
from qiskit_optimization.algorithms import MinimumEigenOptimizer

# useful additional packages
import matplotlib.pyplot as plt
import matplotlib.axes as axes


algorithm_globals.random_seed = 432
seed = 42

# setup aqua logging
# set_qiskit_aqua_logging(logging.DEBUG)  # choose INFO, DEBUG to see the


def sample_graph_with_weights() -> nx.Graph:
    """Returns a sample graph with weights"""
    graph = nx.Graph()
    graph.add_nodes_from(range(4))
    graph.add_weighted_edges_from(
        [
            (0, 1, 23.0),
            (0, 2, 11.0),
            (1, 2, 92.0),
            (2, 3, 61.0),
        ]
    )
    # print the graph
    print("graph:", graph.nodes(), graph.edges(data=True))
    # draw the graph
    pos = nx.spring_layout(graph)
    colors = ["r" for node in graph.nodes()]
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(
        graph,
        node_color=colors,
        node_size=600,
        alpha=0.8,
        ax=default_axes,
        pos=pos,
    )
    return graph


def add_missing_edges(G: nx.Graph) -> nx.Graph:
    """Adds edges to a graph

    Args:
        G (nx.Graph): Graph to add edges to
        edges (List[Tuple[int, int, float]]): List of edges to add

    Returns:
        nx.Graph: Graph with edges added
    """
    # Get the non_edges
    non_edges = nx.non_edges(G)

    # Add large weight to non_edges
    non_edges = [(u, v, 10000.0) for (u, v) in non_edges]
    print(non_edges)
    # Add all the non_edges to the graph
    G.add_weighted_edges_from(non_edges)
    return G


def draw_tsp_solution(G, order, colors, pos):
    """Draws the solution of the TSP problem.

    Args:
        G (_type_): _description_
        order (_type_): _description_
        colors (_type_): _description_
        pos (_type_): _description_

    Credit: https://qiskit.org/documentation/stable/0.25/tutorials/optimization/6_examples_max_cut_and_tsp.html
    Modified by: Ricky Young (uameed)
    """
    G2 = nx.DiGraph()
    G2.add_nodes_from(G)
    n = len(order)
    for i in range(n):
        j = (i + 1) % n
        G2.add_edge(order[i], order[j], weight=G[order[i]][order[j]]["weight"])
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(
        G2,
        node_color=colors,
        edge_color="b",
        node_size=600,
        alpha=0.8,
        ax=default_axes,
        pos=pos,
    )
    edge_labels = nx.get_edge_attributes(G2, "weight")
    nx.draw_networkx_edge_labels(G2, pos, font_color="b", edge_labels=edge_labels)


def _convert_to_tsp_problem(G: nx.Graph) -> Tsp:
    """_summary_

    Args:
        G (nx.Graph): _description_

    Returns:
        Tsp: _description_
    """
    # Create a tsp instance
    tsp = Tsp(G)

    # Convert the problem to a quadratic program
    qp = tsp.to_quadratic_program()
    print(qp.prettyprint())
    qp2qubo = QuadraticProgramToQubo()
    qubo = qp2qubo.convert(qp)
    qubitOp, offset = qubo.to_ising()
    return qubitOp, offset, qp, qubo, tsp


def run_tsp_on_simulator(G: nx.Graph) -> Tuple[List, MinimumEigenOptimizer]:
    """Runs the TSP on a qiskit statevector simulator"""
    qubitOp, offset, _qp, qubo, tsp = _convert_to_tsp_problem(G)
    # Convert the problem to an ising model

    # Solve the quadratic program using the exact eigensolver

    # Making the Hamiltonian in its full form and getting the lowest eigenvalue and eigenvector
    ee = NumPyMinimumEigensolver()

    result = ee.compute_minimum_eigenvalue(qubitOp)

    print("energy:", result.eigenvalue.real)
    print("tsp objective:", result.eigenvalue.real + offset)
    x = tsp.sample_most_likely(result.eigenstate)
    print("feasible:", qubo.is_feasible(x))
    z = tsp.interpret(x)
    print("solution:", z)
    return z, result


def run_tsp_on_hardware(
    G: nx.graph, sampler: Sampler, maxiter: int = 300, reps: int = 5
) -> Tuple[np.ndarray, SamplingMinimumEigensolverResult]:
    """Runs the TSP on a qiskit hardware"""
    qubitOp, offset, _qp, qubo, tsp = _convert_to_tsp_problem(G)

    # Convert the problem to an ising model
    optimizer = SPSA(maxiter=maxiter)
    ry = TwoLocal(qubitOp.num_qubits, "ry", "cz", reps=reps, entanglement="linear")
    vqe = SamplingVQE(sampler=sampler, ansatz=ry, optimizer=optimizer)

    result = vqe.compute_minimum_eigenvalue(qubitOp)

    print("energy:", result.eigenvalue.real)
    print("time:", result.optimizer_time)
    x = tsp.sample_most_likely(result.eigenstate)
    print("feasible:", qubo.is_feasible(x))
    z = tsp.interpret(x)
    print("solution:", z)

    return z, result
