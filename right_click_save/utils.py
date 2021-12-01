import web3

from . import the_graph
from .token import Token


def get_tokens(*addresses):
    for address in addresses:
        yield from Token.from_address(address)


def resolve_addresses(*addresses):
    retval = set()
    for address in addresses:
        if web3.Web3.isAddress(address):
            retval.add(address)
        if retrieved_address := the_graph.query_ens(address):
            retval.add(retrieved_address)
    return retval
