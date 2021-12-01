import base64
import binascii
import json

import requests

from . import the_graph


__all__ = ("Token",)


class Token:
    def __init__(self, address, id_, meta_data):
        self.address = address
        self.id_ = int(id_, 16)
        self.meta_data = meta_data

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.address}, {self.id_}]>"

    @classmethod
    def from_address(cls, address):
        data = the_graph.query_erc721(address)
        for account in data["accounts"]:
            for erc721_token in account["tokens"]:
                if token_uri := erc721_token["uri"]:
                    token_address, token_id = erc721_token["id"].split("-")
                    base64_data = token_uri.split(",", 1)[-1]
                    try:
                        # Check of the metadata is embedded on-chain
                        encoded_data = base64.b64decode(base64_data)
                    except binascii.Error:
                        # Our decode attempt failed, the token uri
                        # must just be a pointer to an off-chain url
                        url = base64_data
                        r = requests.get(url)
                        r.raise_for_status()
                        meta_data = r.json()
                    else:
                        decoded_data = encoded_data.decode(encoding="utf-8")
                        meta_data = json.loads(decoded_data)
                    yield cls(token_address, token_id, meta_data)
