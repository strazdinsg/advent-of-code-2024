use_example_input = False


def main():
    input_file_name = "example23.txt" if use_example_input else "input23.txt"
    network = read_input(input_file_name)
    three_cliques = find_three_node_cliques(network)
    possible_admin_cliques = filter_cliques_starting_with(three_cliques, "t")
    print(f"Part1: {len(possible_admin_cliques)} possible admin cliques")
    largest_clique = find_largest_clique(network)
    largest_clique_alphabetical = get_part2_answer(largest_clique)
    print(f"Part 2: largest clique = {largest_clique_alphabetical}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        neighbors = {}
        line = f.readline().strip()
        while line != "":
            u, v = line.split("-")
            if u not in neighbors:
                neighbors[u] = set()
            if v not in neighbors:
                neighbors[v] = set()
            neighbors[u].add(v)
            neighbors[v].add(u)
            line = f.readline().strip()
        return neighbors


def find_three_node_cliques(neighbors):
    cliques = set()
    for u in neighbors:
        for v in neighbors[u]:
            if u < v:
                for w in neighbors[u]:
                    if v < w and w in neighbors[v]:
                        cliques.add((u, v, w))
    return cliques


def filter_cliques_starting_with(cliques, prefix):
    return {(u, v, w) for (u, v, w) in cliques if u.startswith(prefix) or v.startswith(prefix) or w.startswith(prefix)}


def find_largest_clique(neighbors):
    cliques = find_cliques(neighbors)
    max_clique = set()
    for clique in cliques:
        if len(clique) > len(max_clique):
            max_clique = clique
    return max_clique


def find_cliques(graph):
    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, cliques)
    return cliques


def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(R)
        return
    for v in list(P):
        bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph,
            cliques
        )
        P.remove(v)
        X.add(v)


def get_part2_answer(largest_clique):
    return ",".join(sorted(largest_clique))


if __name__ == "__main__":
    main()
