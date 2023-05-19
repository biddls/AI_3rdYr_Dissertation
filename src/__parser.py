import json
from glob import glob
from typing import Generator, Union

def contract_parser(
    path: Union[str, Generator[str, None, None]]
) -> Generator[dict, None, None]:
    """
    Parses Solidity contract files and yields the parsed dictionaries for each contract.

    Args:
    - path: str or Generator[str, None, None]
        If str, a glob pattern used to match contract file(s) to parse. If Generator[str, None, None],
        an iterable that yields paths to contract files.

    Yields:
    - dict: the parsed dictionary for a contract file.
    """
    path = glob(path) if isinstance(path, str) else path

    # starts iterating over the loaded contract file locations
    for contract in path:
        # loads in contract
        with open(contract, 'r') as f:
            contract = json.load(f)

        # removes unneeded keys
        contract = contract["children"]

        # iterates over the main parts of the contract file
        for x in contract:
            if x["type"] == "ImportDirective":
                # cleans out stuff not needed to show an import
                contract[1].pop("symbolAliases")
                contract[1].pop("unitAlias")
        yield contract

if __name__ == '__main__':
    a = contract_parser('contracts_parsed/Cont2.sol.json')
    print(json.dumps(next(a), indent=2))
