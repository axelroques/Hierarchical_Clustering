
from .hierarchy import Hierarchy
from .cluster import Cluster
from .tree.tree import Tree

import numpy as np


class HierarchicalClustering:

    def __init__(self, matching_sequences) -> None:
        """
        Input:
            - matching_sequences = sequences of matching dots returned
            by the Dotplots generation algorithm. Each sequence consists
            in a succession of AoI.
        """

        # Initialize clusters
        self.clusters = self._getClusters(matching_sequences)

    def process(self):
        """
        Clusterization process.
        """

        # Create a hierarchy instance
        hierarchy = Hierarchy(self.clusters)

        # Start recursive clustering
        self.clusters = self._recursiveClustering(hierarchy, self.clusters)

        return self.clusters

    @staticmethod
    def _getClusters(sequences):
        """
        Return a list of clusters from a list of matching sequences.
        """
        return [
            Cluster([sequence], sequence, 0) for sequence in sequences
        ]

    @staticmethod
    def _recursiveClustering(hierarchy, clusters):
        """
        Recursively clusterize the sequences.
        """

        # Return if only one cluster remains
        if len(clusters) == 1:
            return clusters

        # Compute distances with a distance matrix
        M, match_counter = HierarchicalClustering._computeDistances(clusters)
        print('Distance matrix =\n', M)

        # Find the two closest clusters
        indices = np.unravel_index(np.argmin(M, axis=None), M.shape)
        print('indices =', indices)

        # Create a new cluster with the closest clusters
        new_cluster = Cluster(
            [clusters[i] for i in indices],
            HierarchicalClustering._chooseClusterSequence(
                clusters, match_counter, indices
            ),
            M[indices]
        )

        # Get a new list of clusters for the next iteration
        new_clusters = [new_cluster] + [
            cluster for i, cluster in enumerate(clusters)
            if i not in indices
        ]

        # Update hierarchy
        hierarchy.addCluster(new_cluster)

        return HierarchicalClustering._recursiveClustering(
            hierarchy, new_clusters
        )

    @staticmethod
    def _computeDistances(clusters):
        """
        Compute distances between each pairs of sequences in the tree.
        The notations used are those employed in the orignal article.
        """

        # Initialize distance matrix
        n = len(clusters)
        M = np.zeros((n, n))

        # Initialize a dictionary that counts the number of matches between
        # a sequence and all others
        match_counter = {i: 0 for i in range(len(clusters))}

        # Create a generalized suffix tree with all input cluster sequences
        tree = Tree({
            index: cluster.sequence for index, cluster in enumerate(clusters)
        })

        try:
            # Largest number of sequentially matching AoIs in the entire dataset
            _, maxMatchLength, _ = tree.common_substrings()[0]

        # No match between the clusters
        except IndexError:
            # What should be done here?
            return

        # Pairwise distance computation
        #*- Probably not very efficient -*#
        for i in range(n):
            for j in range(i, n):

                # Diagonal values
                if i == j:
                    M[i, j] = np.inf
                    continue

                subtree = Tree({
                    i: clusters[i].sequence,
                    j: clusters[j].sequence
                })

                # Find matches between the pair
                results = subtree.common_substrings()
                try:
                    # Number of sequentially matching AoIs between the pair
                    _, matchLength, _ = results[0]

                    # Distance computation
                    #*- Personal change here (1-...) -*#
                    distance = 1 - matchLength / maxMatchLength

                    # Update counter
                    match_counter[i] += len(results)
                    match_counter[j] += len(results)

                # No match between the clusters
                except IndexError:
                    distance = np.inf

                M[i, j] = distance

        # Fill lower triangle of the symmetric matrix
        M = M + M.T

        return M, match_counter

    @staticmethod
    def _chooseClusterSequence(clusters, match_counter, indices):
        """
        According to the article:
        "The merged cluster is assigned the child sequence that matches the 
        most other sequences in the dataset".

        This choice is the sole purpose of the 'match_counter'. 
        """

        if match_counter[indices[0]] >= match_counter[indices[1]]:
            return clusters[indices[0]].sequence

        else:
            return clusters[indices[1]].sequence
