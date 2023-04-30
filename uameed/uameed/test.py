# Sample run of TSP

from tsp import (
    run_tsp_on_simulator,
    sample_graph_with_weights,
    run_tsp_on_hardware,
    add_missing_edges,
)

from qiskit_machine_learning.kernels import FidelityQuantumKernel

FidelityQuantumKernel


graph = sample_graph_with_weights()

graph = add_missing_edges(graph)
# z, result = run_tsp_on_simulator(graph)

# Sample run of TSP on hardware
# z, result = run_tsp_on_hardware(graph)


from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler

service = QiskitRuntimeService(
    channel="ibm_quantum", instance="ibm-q-startup/qbraid/reservations"
)


options = {
    "max_execution_time": 1500,
    "instance": "ibm-q-startup/qbraid/reservations",
}


with Session(
    service,
    backend="ibmq_guadalupe",
) as session:
    sampler = Sampler(session=session, options=Options(options))

    # Sample run of TSP on hardware
    z, result = run_tsp_on_hardware(graph, sampler)
    print(result)
    print(z, "result")
    print("done")
