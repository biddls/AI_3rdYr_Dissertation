# https://github.com/florian1345/python-solidity-parser
# pip install 'solidity_parser @ '
from glob import glob
import json
from solidity_parser import parser
from typing import Callable, Generator


def get_contracts(
        path: [
            str, Generator[str, None, None],
            Callable[
                [str],
                list[str]
            ]
        ],
        save: bool = False
) -> Generator[dict, None, None]:
    # type checking and handling
    path = glob(path) if isinstance(path, str) else path
    path = path() if isinstance(path, Callable) else path

    # starts itterating over the contract file locations
    for contract in path:
        # parses the contract
        cont = parser.parse_file(contract, loc=False)
        # converts the contract to a dictionary
        cont = dict(cont)
        # TODO: add some sort of sorting here so smaller values/keys are at the top
        if save:
            # converts the contract to a json string
            cont = json.dumps(contract, indent=4)
            # parses out the name of the contract
            name = contract.replace('/', '\\').split('\\')[-1]
            # saves the contract to a json file
            with open(f'contracts_parsed/{name}.json', 'w+') as f:
                f.writelines(cont)
        yield cont


if __name__ == '__main__':
    a = get_contracts('../contracts/contracts/*.sol', save=True)
    b = get_contracts(glob('../contracts/contracts/*.sol'), save=True)
    print(list(a) == list(b))
