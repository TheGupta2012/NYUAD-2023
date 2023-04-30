from strawberryfields.apps import data, sample, subgraph, plot
import plotly
import networkx as nx


class GBSOptimizer:
    def __init__(self, N=30, K=8, graph="base"):
        self.N = N
        self.K = K
        self.original_graph = graph
        # this will be the collapsed graph
        self.collapsed_graph = None
        self.clusters = None

    def get_init_subgraphs(self):
        pass

    def get_subgraphs(self, init_subgraphs, graph, K):
        # get the nodes from the qml search solver

        # build a subgraph from the nodes that we get
        # using the original graph

        # cluster is gonna be a nx.graph object

        # 1. take the node list of the cluster
        # 2. use that nodes list to build the subgraph using the original graph's connectivity
        init_subgraphs = self.get_init_subgraphs(self.K, self.N)
        # backend or not?
        return self.get_subgraphs(init_subgraphs, self.original_graph, self.K)

    def get_collapsed_graph(self, clusters):
        new_graph = None
        edge_pairing = {}  # {edge : (start_cluster_node, end_cluster_node)}
        # keyed by the edge and value  is the node in the start cluster and end in the node in the end cluster

        for cluster in clusters:
            nodes = set()  # of these nodes in this cluster
            # for each node in this cluster , remove the
            # nodes from the original graph and
            # if you're removing an EDGE WHICH HAS THE OUTGOING NODE
            # NOT IN CLUSTER, add that edge to this new node

        return new_graph, edge_pairing

    def calculate_cycle(self, graph):
        # this will get a subgraph and return a cycle nx.graph object
        # constructed with this subgraph
        pass

    def find_subgraphs_routes(self):
        subgraph_routes = []
        for cluster in self.clusters:
            subgraph_routes.append(self.calculate_cycle(cluster))
        return subgraph_routes

    # after the edge pairing is done, we will need to find the
    # dijkstra routes
    def find_dijkstra_route(self, source, destination, graph, edge_pairing):
        # will return the min weight and the path to the
        # destination node
        pass

    def get_cost(self, subgraph_routes, global_route):
        # start from a node in the global tsp route

        total_cost = 0

        # cluster = self.clusters[0]

        # # there is going to be a cluster
        # i = 0
        # length = len(global_route)
        # cluster_id = None

        # for i in range(length):
        #     cluster_id = i
        #     edge_1 = self.edge_pairing[global_route.edges[i]]
        #     edge_2 = self.edge_pairing[global_route.edges[(i + 1) % length]]

        #     # edge1    u1 ------ v1 (cluster) u2 ------ v2
        #     # how to get the cluster?
        #     node_a = edge_1[1]  # node in the cluster
        #     node_b = edge_2[0]  # again, node in the cluster

        #     cluster_graph = self.subgraphs[cluster_id]
        #     cluster_route = subgraph_routes[cluster_id]

        #     # get the edges of the subgraph route which contains node_a
        #     # and node_b
        #     start_a_nodes = []
        #     start_a_edges = []
        #     for edge in cluster_route.edges:
        #         if node_a in edge:
        #             if node_a == edge[0]:
        #                 start_a_nodes.append(edge[1])
        #             else:
        #                 start_a_nodes.append(edge[0])

        #             start_a_edges.append(edge)

        #     start_b_nodes = []
        #     start_b_edges = []
        #     for edge in subgraph_routes[cluster_id]:
        #         if node_b in edge:
        #             if node_b in edge:
        #                 if node_b == edge[1]:
        #                     start_b_nodes.append(edge[0])
        #                 else:
        #                     start_b_nodes.append(edge[1])
        #             start_b_edges.append(edge)

        #     cycle_cost = sum([edge.weight for edge in cluster_route.edges])

        #     cost_1 = cycle_cost - start_a_edges[1].weight + self.find_dijkstra_route(start_a_nodes[], node_b, cluster_graph)
        return total_cost

    # Quantum enabled large scale routing with applications in lo

    def solve(self):
        # 1. Find the subgraphs
        self.subgraphs = self.get_subgraphs()

        # 2. Find the subgraph routes
        subgraph_tsp_routes = self.find_subgraph_routes()

        # 3. Collapse the graph
        self.collapsed_graph, self.edge_pairing = self.get_collapsed_graph(
            self.subgraphs
        )

        # 4. Make tsp route for big graph
        global_tsp_route = self.calculate_cycle(self.collapsed_graph)

        return self.get_cost(subgraph_tsp_routes, global_tsp_route)
