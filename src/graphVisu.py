from matplotlib.pylab import show
import networkx as nx


def funcParse(func: str) -> str:
    return parse(func, True)


def varParse(var: str) -> str:
    return parse(var, False)


def parse(_in: str, func: bool) -> str:
    _in = _in.split('.')
    _in.insert(1, 'F' if func else 'V')
    _in = '.'.join(_in)
    return _in


class graphManager:
    def __init__(self, draw: bool = False):
        self.__G = nx.MultiDiGraph()
        self.__edge_labels = {}
        self.__data = {}
        self.__draw = draw

    def __enter__(self):
        return self

    def addContract(self, cont: str):
        self.__G.add_node(cont)
        if cont in self.__data.keys():
            raise Exception(f"Contract {cont} already exists")  # TODO: custom exception
        else:
            self.__data[cont] = {}

    def addFunction(self, cont: str, func: str):
        self.__add_entity(cont, func, True)

    def addStateVariable(self, cont: str, var: str):
        self.__add_entity(cont, var, False)

    def __add_entity(self, cont: str, name: str, is_function: bool):
        full_name = f"{cont}.{'F' if is_function else 'V'}.{name}"
        self.__G.add_node(full_name)
        if cont in self.__data.keys():
            if name in self.__data[cont].keys():
                raise Exception(f"{'Function' if is_function else 'Variable'} {name} already exists")
            else:
                self.__data[cont][name] = {}
        else:
            raise Exception(f"Contract {cont} not found")
        self.__addEdge(cont, full_name, 'contains')

    def funcCallsFunc(self, func1: str, func2: str):
        self.__addEdge(funcParse(func1), funcParse(func2), 'calls')

    def funcReadsVar(self, func1: str, var1: str):
        self.__addEdge(funcParse(func1), varParse(var1), 'reads')

    def funcWritesVar(self, func1: str, var1: str):
        self.__addEdge(funcParse(func1), varParse(var1), 'writes')

    def __addEdge(self, node1: str, node2: str, label: str):
        self.__G.add_edge(node1, node2)
        self.__edge_labels[(node1, node2)] = label

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__draw:
            self.draw()
        else:
            pass

    def draw(self):
        # sets the layout of the graph

        # keys = list(self.__data.keys())
        # nlist = [
        #     list(cont) + [f"{cont}.{elem}"
        #                   for elem in list(self.__data[cont].keys())]
        #     for cont in keys
        # ]
        # pos = nx.shell_layout(self.G, nlist)

        pos = nx.circular_layout(sorted(self.__G.nodes()))

        # TODO: colours the nodes
        # color_map = []
        # for node in G:
        #     if node < 10:
        #         color_map.append('blue')
        #     else:
        #         color_map.append('green')
        # nx.draw(G, node_color=color_map, with_labels=True)

        # draws the graph
        nx.draw(
            self.__G,
            pos,
            node_color='pink',
            node_size=1000,
            alpha=1,
            with_labels=True
            # connectionstyle='arc3, rad = 0.05'
        )

        # draws the edge labels
        nx.draw_networkx_edge_labels(
            self.__G,
            pos,
            self.__edge_labels,
            rotate=False,
            label_pos=0.25,
            bbox=dict(boxstyle='round', fc='white', alpha=1)
        )

        # shows the graph
        show()


if __name__ == '__main__':
    gm = graphManager()
    gm.addContract('A')
    gm.addContract('B')
    gm.addFunction('A', 'g')
    gm.addFunction('B', 'h')
    gm.addStateVariable('A', 'x')
    gm.addStateVariable('B', 'y')
    gm.funcCallsFunc('A.g', 'B.h')
    gm.funcReadsVar('A.g', 'A.x')
    gm.funcReadsVar('A.g', 'A.x')
    gm.funcWritesVar('B.h', 'B.y')
    gm.draw()