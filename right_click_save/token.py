import logging

from . import the_graph, utils


__all__ = ("Token",)


log = logging.getLogger(__name__)


class Token:
    def __init__(self, address, id_, metadata):
        self.address = address
        self.id_ = int(id_, 16)
        self.metadata = metadata

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.address}, {self.id_}]>"

    @classmethod
    def from_address(cls, address):
        data = the_graph.query_erc721(address)
        for account in data["accounts"]:
            for erc721_token in account["tokens"]:
                # Standard ERC-721 NFT
                if token_uri := erc721_token["uri"]:
                    token_address, token_id = erc721_token["id"].split("-")
                    metadata = utils.extract_erc721_metadata(token_uri)
                    yield cls(token_address, token_id, metadata)
                else:
                    log.warning("No URI found in %s", erc721_token)
