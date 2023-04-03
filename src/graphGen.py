from networkx import MultiDiGraph
from graphVisu import graphManager
from __parser import contract_parser
from json import dumps
from typing import Callable, Generator


def jd(x):
    print(dumps(x, indent=2))


# finds the first value in an array of dictionaries
def findInArray(
        array: [dict],
        key: str,
        finder,#: bool | Callable[[dict], bool],
        value: str
) -> (any, int):
    # iterates over the array
    for index, item in enumerate(array):
        # checks if the key is in the item
        if key in item.keys():
            # checks if the finder is a boolean
            if isinstance(finder, bool):
                # returns the value targeted
                return item[value], index
            # checks if the finder function returns a true
            if finder(item):
                # if the finder gets its value then return it
                return item[value], index
    # if nothing is found then return None
    return None, None


def findName(array: [dict]) -> str:
    _name, _ = findInArray(
        array,
        'type',
        lambda x: x['type'] == 'ContractDefinition',
        'name')

    if _name is None:
        raise Exception('No contract name found')
    return _name


def getSubNodes(array: [dict]) -> [dict]:
    _subNodes, _ = findInArray(array, 'subNodes', True, 'subNodes')
    if _subNodes is None:
        raise Exception('No subNodes found')
    return _subNodes


# "type":"FunctionCall"
#
def search_dict(
        dictionary: dict,
        key: str
) -> list:
    results = []
    for k, v in dictionary.items():
        if k == key:
            results.append(v)
        elif isinstance(v, dict):
            sub_results = search_dict(v, key)
            if sub_results:
                results.extend(sub_results)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    sub_results = search_dict(item, key)
                    if sub_results:
                        results.extend(sub_results)
    return results


def genGRaph(
    path: [
        str,
        Generator[str, None, None]
    ],
    draw: bool = False
) -> list[(str, str, dict[str, str])]:
    with graphManager(draw=draw) as G:
        for cont in contract_parser(path):
            name = findName(cont)
            G.addContract(name)

            subNodes = getSubNodes(cont)
            # jd(subNodes)
            # getting the type of the subNode
            var, _ = findInArray(subNodes, 'type', lambda _dict: 'StateVariableDeclaration' == _dict['type'],
                                 'variables')
            for variable in var:
                if (
                        variable['visibility'] in ['public', 'external']
                        and not variable['isDeclaredConst']
                        and not variable['isDeclaredImmutable']
                ):
                    G.addStateVariable(name, variable['name'])

            # filters out all the constructor functions
            noConst = []
            for subNode in subNodes:
                isConst, i = findInArray([subNode], 'type', lambda _dict: 'FunctionDefinition' == _dict['type'],
                                         'isConstructor')
                # print(isConst, i)
                if isConst is False:
                    noConst.append(subNode)

            # jd(noConst)
            for elem in noConst:
                # gets all the outermost 'expression' keys
                result = search_dict(elem, 'expression')
                func_name = elem['name']
                G.addFunction(name, func_name)
                for res in result:
                    res = res.copy()
                    # jd(res)
                    # jd(res['type'])
                    if res['type'] == 'FunctionCall':
                        for arg in res['arguments']:
                            try:
                                if arg['left']['type'] == 'FunctionCall':
                                    cont = arg['left']['expression']['expression']['name']
                                    func = arg['left']['expression']['memberName']
                                    G.funcReadsVar(f"{name}.{func_name}", f"{cont}.{func}")
                            except KeyError:
                                pass
                                # print(cont, func)
                    elif res['type'] == 'BinaryOperation':
                        if res['left']['type'] == 'Identifier':
                            G.funcWritesVar(f"{name}.{func_name}", f"{name}.{res['left']['name']}")
    return [(x1, x2, x4) for x1, x2, x3, x4 in G.getGraph()[0].edges.data(keys=True)]


if __name__ == '__main__':
    graph = genGRaph('contracts_parsed/**.sol.json', draw=True)
    for x in graph:
        print(x)
