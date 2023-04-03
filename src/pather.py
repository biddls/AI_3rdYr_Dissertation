from typing import Generator


def __p(
        _x: any,
        logging: bool = False
) -> None:
    if logging:
        print(_x)


def graphTraversal(
        _graph: list[(str, str, dict[str, str])],
        _current: list[str],
        _maxDepth: int or float = 10  # can be set to float('inf') to perpetually search
) -> Generator[list[str], None, None]:
    # find the functions that write to the target
    edges: list[(str, str, dict[str, str])] = []
    for edge in filter(lambda _x: _x[2]['label'] != 'contains', _graph):
        # print(edge, _current)
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

    # ensures that the shallowest paths are returned first
    for edge in edges:
        temp = variableFilter(_current + [edge])
        if temp != variableFilter(_current):
            yield temp
        __p(f"{_current + [edge] = }")

    for edge in edges:
        a = graphTraversal(_graph, _current + [edge], _maxDepth - 1)
        for _x in a:
            yield variableFilter(_x)


def variableFilter(
        _list: list[str]
) -> list[str]:
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
