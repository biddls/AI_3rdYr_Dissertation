from typing import Generator, Optional, List, Dict
import brownie.typing
from brownie import accounts, Contract, network, chain, rpc
from loader import get_contracts
from graphGen import genGRaph
from glob import glob
import json
from pather import graphTraversal

network.connect('development')


def deploy(
        _byte_code: str,
        _param: Optional[str] = None
) -> brownie.typing.TransactionReceiptType:
    """
    Deploy a smart contract to the blockchain.

    Args:
        _byte_code: The bytecode of the contract to be deployed.
        _param: Optional parameter to pass to the contract constructor.

    Returns:
        The transaction receipt of the deployment.
    """
    if _param is not None:
        _byte_code += "000000000000000000000000" + _param[2:]

    _comp = accounts[0].transfer(data=_byte_code, silent=True)

    return _comp


def link_contracts(
        _contracts: List[str],
        log: bool = False
) -> Dict[str, Contract]:
    """
    Link the contracts to their corresponding bytecode and deploy them to the blockchain.

    Args:
        _contracts: A list of contract names to be deployed.
        log: A boolean flag indicating whether to print log messages.

    Returns:
        A dictionary of deployed contract instances with the contract name as the key.
    """
    if log:
        _p = print
    else:
        _p = lambda x: None

    # get the abi for each contract
    comped1 = glob('../contracts/artifacts/contracts/*.sol/*.json')
    comped2 = glob('../contracts/artifacts/contracts/*.sol/*.dbg.json')

    comped: List[str] = list(set(comped1) - set(comped2))

    if not len(comped) == len(_contracts):
        raise Exception("Contract count mismatch")

    contractMapping = {}
    last = None
    comped: List[str] = list(sorted(comped))

    for comp, cont in zip(comped, _contracts):
        _temp = f"Deployed: {cont} from {comp}"
        with open(str(comp), 'r') as f:
            comp = json.load(f)

        byte_code = comp['bytecode']
        abi = comp['abi']
        if last is not None:
            comp = deploy(byte_code, _param=last)
        else:
            comp = deploy(byte_code)

        last = comp.contract_address
        comp: Contract = Contract.from_abi(cont, last, abi)

        contractMapping[cont] = comp
        _p(f"{_temp} at {last}")

    return contractMapping


def manager(
        _contracts: Dict[str, brownie.network.contract.Contract],
        _path: Generator[List[str], None, None],
        _target: brownie.typing.TransactionReceiptType
) -> List[str] or None:
    """
    Given a list of contracts, a graph traversal path and a target value,
    this function tests each path, in reverse order, to determine whether
    it leads to the target value. If a successful path is found, it is returned.

    Args:
        _contracts: A dictionary containing the contracts to be tested.
        _path: A generator object containing the paths to be tested.
        _target: The target value to be reached.

    Returns:
        - If a path to the target is found, the function returns the path as a list of strings.
        - If a path to the target is not found, the function returns None.
    """
    # current target value
    _currentTarget = _target()
    print("\n")
    for x in _path:
        x.reverse()
        print(f"Testing Path: {x}")
        # test path
        for i in x:
            cont = _contracts[i.split('.')[0]]
            func = i.split('.')[-1]
            func = getattr(cont, func)
            try:
                print(f"Calling {func} {i}")
                func({'from': accounts[0]})
            except brownie.exceptions.VirtualMachineError as e:
                if 'revert' not in e.message:
                    raise e
                else:
                    break

        if _currentTarget != _target():
            return x
        # revert to snapshot
        chain.revert()

    return None


if __name__ == "__main__":
    # get the contracts parsed and into a graph
    get_contracts('../contracts/contracts/*.sol', save=True)
    graph: list[(str, str, dict[str, str])] = genGRaph('contracts_parsed/**.sol.json')

    # begin analysing the graph and match it to the contracts
    contracts: list[str] = []

    # get list of contracts from graph
    for edge in graph:
        if edge[2]['label'] == 'contains':
            if edge[0] not in contracts:
                contracts.append(edge[0])

    # deploy the contracts
    contracts: Dict[str, Contract] = link_contracts(contracts, log=True)

    # creates a snapshot of the current state of the blockchain
    chain.snapshot()

    # define the target
    target = contracts['cont3'].freed

    # instantiate the graph traversal algorithm
    path = graphTraversal(graph, ['cont3.v.freed'])
    path = manager(contracts, path, target)

    # print found path
    print(f"Found path: {path}")

    network.disconnect()
    # rpc.disconnect()
