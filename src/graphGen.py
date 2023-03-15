from graphVisu import graphManager
from parser import contract_parser
from json import dumps
from typing import Callable


# finds a value in an array of dictionaries
def findInArray(
        array: [dict],
        key: str,
        finder: bool | Callable[[dict], bool],
        value: str
) -> any:
    # iterates over the array
    for item in array:
        # checks if the key is in the item
        if key in item.keys():
            # checks if the finder is a boolean
            if isinstance(finder, bool):
                # returns the value targeted
                return item[value]
            # checks if the finder function returns a true
            if finder(item):
                # if the finder gets its value then return it
                return item[value]
    # if nothing is found then return None
    return None


def findName(array: [dict]) -> str:
    name = findInArray(
        array,
        'type',
        lambda x: x['type'] == 'ContractDefinition',
        'name')

    if name is None:
        raise Exception('No contract name found')
    return name


def getSubNodes(array: [dict]) -> [dict]:
    subNodes = findInArray(array, 'subNodes', True, 'subNodes')
    if subNodes is None:
        raise Exception('No subNodes found')
    return subNodes


if __name__ == '__main__':
    with graphManager(draw=True) as G:
        for cont in contract_parser('contracts_parsed/*.sol.json'):
            # print(dumps(cont, indent=2))
            name = findName(cont)
            G.addContract(name)

            subNodes = getSubNodes(cont)

            # getting the type of the subNode
            var = findInArray(subNodes, 'type', lambda x: 'Variable' in x['type'], 'variables')
            for variable in var:
                if (
                        variable['visibility'] in ['public', 'external']
                        and not variable['isDeclaredConst']
                        and not variable['isDeclaredImmutable']
                ):
                    G.addStateVariable(name, variable['name'])
