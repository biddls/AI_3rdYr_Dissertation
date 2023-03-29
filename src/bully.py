import pytest
from brownie import accounts, Contract, config, network
from loader import get_contracts
from graphGen import genGRaph
from glob import glob
import json

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

    print(conts)

    # get the abi for each contract
    abi = []
    comped1 = glob('../contracts/artifacts/contracts/*.sol/*.json')
    comped2 = glob('../contracts/artifacts/contracts/*.sol/*.dbg.json')

    comped = list(set(comped1) - set(comped2))

    assert len(comped) == len(conts)

    contracts = {}
    last = None
    for comp, cont in zip(comped, conts):
        with open(comp, 'r') as f:
            comp = json.load(f)

        byte_code = comp['bytecode']
        comp = accounts[0].transfer(data=byte_code)
        if last is not None:
            comp = Contract.from_abi(cont, comp.address(), abi)
        last = comp

        contracts[cont] = comp



    # deployment_bytecode = "0x6103f056600035601c52740100..."
    # br.accounts[0].transfer(data=deployment_bytecode)
    # br.Contract.from_abi("Token", "0x79447c97b6543F6eFBC91613C655977806CB18b0", abi)

