from brownie import accounts, Contract, network
from loader import get_contracts
from graphGen import genGRaph
from glob import glob
import json

network.connect('development')

def deploy(_byte_code, _param=None):
    if _param is not None:
        _byte_code += "000000000000000000000000" + _param[2:]

    _comp = accounts[0].transfer(data=_byte_code)

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
    abi = []
    comped1 = glob('../contracts/artifacts/contracts/*.sol/*.json')
    comped2 = glob('../contracts/artifacts/contracts/*.sol/*.dbg.json')

    comped = list(set(comped1) - set(comped2))

    assert len(comped) == len(_contracts)

    contracts = {}
    last = None
    comped = list(sorted(comped))

    for comp, cont in zip(comped, _contracts):
        _p(f"Deploying: {cont} from {comp}")
        with open(comp, 'r') as f:
            comp = json.load(f)

        byte_code = comp['bytecode']
        if last is not None:
            comp = deploy(byte_code, _param=last)
        else:
            comp = deploy(byte_code)

        last = comp.contract_address
        comp = Contract.from_abi(cont, last, abi)

        contracts[cont] = comp
        _p(f"Done: {cont} at {last}")

    return contracts


if __name__ == "__main__":
    # get the contracts parsed and into a graph
    get_contracts('../contracts/contracts/*.sol', save=True)
    graph = genGRaph('contracts_parsed/**.sol.json')

    # begin analysing the graph and match it to the contracts
    conts: [str] = []
    _graph: [(str, str, int, dict[str, str])] = graph[0].edges.data(keys=True)

    # get list of contracts from graph
    for edge in _graph:
        if edge[3]['label'] == 'contains':
            if edge[0] not in conts:
                conts.append(edge[0])

    conts = link_contracts(conts)
