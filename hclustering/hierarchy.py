
class Hierarchy:

    def __init__(self, clusters) -> None:

        # Initialize node array
        self.nodes = [
            Node(cluster) for cluster in clusters
        ]

    def addCluster(self, cluster):
        """
        Add a cluster to the hierarchy.
        """

        # Find node parents
        parents = self.findClusterParent(cluster)
        print('parents =', parents)

        # Append a Node to the array
        node = Node(cluster, parents)
        self.nodes.append(node)

        # Append a children to the parent
        for parent in node.parents:
            parent.addChild(node)

        return

    def findClusterParent(self, cluster):
        """
        Find parent nodes by cluster constituants.
        """

        for c in cluster.constituants:
            print('test 1 =', c)
            print(self.nodes[0].cluster.sequence)
        nodes = [
            node for node in self.nodes
            if any(
                node.cluster.sequence == cluster.sequence
                for cluster in cluster.constituants
            )
        ]
        print('NODES =', nodes)

        return nodes


class Node:

    def __init__(self, cluster, parents=None):

        # Basic parameters
        self.cluster = cluster
        self.parents = parents
        self.children = []

    def addChild(self, child):
        """
        Append a child to the list.
        """

        self.children.append(child)

        return

    def __repr__(self) -> str:
        return f'{self.cluster}'
