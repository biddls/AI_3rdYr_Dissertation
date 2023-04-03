from typing import Generator
import brownie.typing
from brownie import accounts, Contract, network, chain, rpc
from loader import get_contracts
from graphGen import genGRaph
from glob import glob
import json
from pather import graphTraversal

network.connect('development')


def deploy(
        _byte_code,
        _param=None
) -> brownie.typing.TransactionReceiptType:
    if _param is not None:
        _byte_code += "000000000000000000000000" + _param[2:]

    _comp = accounts[0].transfer(data=_byte_code, silent=True)

    return _comp


def link_contracts(
        _contracts: [str],
        log=False
) -> dict[str, Contract]:
    if log:
        _p = lambda x: print(x)
    else:
        _p = lambda x: None

    # get the abi for each contract
    comped1 = glob('../contracts/artifacts/contracts/*.sol/*.json')
    comped2 = glob('../contracts/artifacts/contracts/*.sol/*.dbg.json')

    comped: [str] = list(set(comped1) - set(comped2))

    if not len(comped) == len(_contracts):
        raise Exception("Contract count mismatch")

    contractMapping = {}
    last = None
    comped = list(sorted(comped))

    for comp, cont in zip(comped, _contracts):
        _temp = f"Deployed: {cont} from {comp}"
        with open(comp, 'r') as f:
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
        _contracts: [str, Contract],
        _path: Generator[list[str], None, None],
        _target: brownie.typing.TransactionReceiptType
) -> list[str] or None:
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
    contracts = link_contracts(contracts, log=True)

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
