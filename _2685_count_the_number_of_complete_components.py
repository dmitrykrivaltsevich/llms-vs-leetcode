# Problem:
# You are given an integer n. There is an undirected graph with n vertices, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting vertices ai and bi.

# Return the number of complete connected components of the graph.

# A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.

# A connected component is said to be complete if there exists an edge between every pair of its vertices.

 

# Example 1:



# Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
# Output: 3
# Explanation: From the picture above, one can see that all of the components of this graph are complete.
# Example 2:



# Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
# Output: 1
# Explanation: The component containing vertices 0, 1, and 2 is complete since there is an edge between every pair of two vertices. On the other hand, the component containing vertices 3, 4, and 5 is not complete since there is no edge between vertices 4 and 5. Thus, the number of complete components in this graph is 1.
 

# Constraints:

# 1 <= n <= 50
# 0 <= edges.length <= n * (n - 1) / 2
# edges[i].length == 2
# 0 <= ai, bi <= n - 1
# ai != bi
# There are no repeated edges.
#
from collections import defaultdict
from typing import List

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP != rootQ:
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)

class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        """
        Count the number of complete connected components in an undirected graph.

        A connected component is a subgraph where there exists a path between any two vertices,
        and no vertex shares an edge with a vertex outside the subgraph. A connected component
        is said to be complete if there exists an edge between every pair of its vertices.

        Args:
            n (int): The number of vertices in the graph.
            edges (List[List[int]]): A list of edges where each edge is represented as [ai, bi].

        Returns:
            int: The number of complete connected components.
        """
        uf = UnionFind(n)
        for u, v in edges:
            uf.union(u, v)

        graph = defaultdict(list)
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        visited = [False] * n
        complete_components_count = 0

        def dfs(node):
            stack = [node]
            component = set()
            while stack:
                current = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    component.add(current)
                    for neighbor in graph[current]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
            return component

        def is_complete(component):
            size = len(component)
            for i in range(size):
                for j in range(i + 1, size):
                    u, v = list(component)[i], list(component)[j]
                    if not uf.connected(u, v):
                        return False
            return True

        # Find all connected components
        for node in range(n):
            if not visited[node]:
                component = dfs(node)
                if is_complete(component):
                    complete_components_count += 1

        return complete_components_count
