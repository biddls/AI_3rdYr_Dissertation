from typing import Generator, List, Tuple, Dict, Union, Any


__logging: bool = False


def __p(
        _x: Any
) -> None:
    """
    Helper function to print the input argument `_x` if `__logging` is True
    """
    if __logging:
        print(_x)


def graphTraversal(
        _graph: List[Tuple[str, str, Dict[str, str]]],
        _current: List[str],
        _maxDepth: Union[int, float] = 10.0
) -> Generator[List[str], None, None]:
    """
    Returns a generator that yields all paths from the target outwards from the smallest path to largest or when the
    max depth is reached
    :param _graph: A list of tuples representing edges in the graph. Each tuple has three elements: the start node,
    the end node, and a dictionary of edge attributes.
    :param _current: A list of strings representing the current node.
    :param _maxDepth: The maximum depth to traverse the graph. Defaults to 10, which can be set to float('inf') to
    perpetually search.
    :return: A generator that yields lists of strings representing the paths from the target outwards.
    """
    edges: List[str] = []
    # find the functions that write to the target
    for edge in filter(lambda _x: _x[2]['label'] != 'contains', _graph):
        # checks if the node is at either end of the edge
        if _current[-1] in edge[:2]:
            # ensuring that the directionality of the graph is adhered to
            # if _current is a variable
            __p(f"Logging: \n{edge[2]['label'] = }\n{_current[-1] = }\n{edge[1] = }")
            if edge[2]['label'] == 'writes' and _current[-1] == edge[1]:
                __p(f"{_current[-1]} is a variable")
                edges.append(edge[0])
            # if _current is a function
            elif edge[2]['label'] == 'reads' and _current[-1] == edge[0]:
                __p(f"{_current[-1]} is a function")
                edges.append(edge[1])
    __p(f"Output:\n{edges = }")

    # the yield statements have to be here so that the paths are returned
    # in the correct order else it becomes a depth first search
    # ensures that the shallowest paths are returned first
    for edge in edges:
        temp = variableFilter(_current + [edge])
        if temp != variableFilter(_current):
            yield temp
        __p(f"{_current + [edge] = }")

    # breaks the recursion if the max depth is reached
    if _maxDepth == 0:
        return

    # recursively calls the function to find the next layer of paths
    for edge in edges:
        a = graphTraversal(_graph, _current + [edge], _maxDepth - 1)
        for _x in a:
            yield variableFilter(_x)


def variableFilter(
        _list: List[str]
) -> List[str]:
    """
    Returns a filtered list that excludes any string that has the string ".v" as its second element.
    :param _list: A list of strings to filter.
    :return: A filtered list of strings.
    """
    try:
        return list(filter(lambda _x: (_x.split('.')[1]) != 'v', _list))
    except TypeError as e:
        print(type(_list))
        print(f"{_list = }")
        raise e


if __name__ == "__main__":
    graph = [
        ('cont1', 'cont1.v.freed', {'label': 'contains'}),
        ('cont1', 'cont1.f.free', {'label': 'contains'}),
        ('cont1.f.free', 'cont1.v.freed', {'label': 'writes'}),
        ('cont2', 'cont2.v.freed', {'label': 'contains'}),
        ('cont2', 'cont2.f.free', {'label': 'contains'}),
        ('cont2.f.free', 'cont1.v.freed', {'label': 'reads'}),
        ('cont2.f.free', 'cont2.v.freed', {'label': 'writes'}),
        ('cont3', 'cont3.v.freed', {'label': 'contains'}),
        ('cont3', 'cont3.f.free', {'label': 'contains'}),
        ('cont3.f.free', 'cont2.v.freed', {'label': 'reads'}),
        ('cont3.f.free', 'cont3.v.freed', {'label': 'writes'})
    ]
    target = ['cont3.v.freed']
    print(f"{target[0] = }")
    path = graphTraversal(graph, target)
    for x in path:
        print(f"{x = }")
