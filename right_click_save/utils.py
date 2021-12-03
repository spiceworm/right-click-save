import base64
import logging
from urllib.parse import urlparse

import json
import requests
import web3
import yaml

from . import the_graph
from .token import Token


log = logging.getLogger(__name__)


def get_tokens(*addresses):
    for address in addresses:
        yield from Token.from_address(address)


def decode_json_response(request_resp):
    try:
        data = request_resp.json()
    except json.JSONDecodeError:
        try:
            # Escape characters from non-standard encodings might be causing decode errors
            data = json.loads(request_resp.content.decode("utf-8-sig"))
        except json.JSONDecodeError:
            # Try parsing the string as yaml which is more flexible. There might be a trailing
            # comma that is not permitted according to the JSON spec.
            data = yaml.safe_load(request_resp.text)
    return data


def extract_erc721_metadata(token_uri):
    """
    This function is used to parse out NFT metadata from the token URI.
    The token URI could be a:
        - URL to a location on the public internet
        - IPFS link
        - On-chain metadata
    """

    def _extract_metadata_from_ipfs(token_uri_):
        """
        Only call this function for an IPFS URI.
        """
        ipfs_id_ = token_uri_.rsplit("ipfs", 1)[-1].lstrip(":/")
        ipfs_gateway_url_ = f"https://ipfs.io/ipfs/{ipfs_id_}"
        return _extract_metadata_from_public_internet_url(ipfs_gateway_url_)

    def _extract_metadata_from_public_internet_url(token_uri_):
        """
        Only call this function for a URI that can be reached from the public internet.
        """
        try:
            r_ = requests.get(token_uri_)
            r_.raise_for_status()
        except requests.RequestException:
            log.warning("Unable to resolve metadata for URI: %s", token_uri_)
            metadata_ = {}
        else:
            metadata_ = decode_json_response(r_)
        return metadata_

    def _extract_metadata_from_onchain(token_uri_):
        """
        Only call this function for a URI that contains on-chain data.
        """
        try:
            content_type_, remainder_ = token_uri_.split(";", 1)
        except ValueError:
            log.error('Unhandled token URI "%s"', token_uri_)
            metadata_ = {}
        else:
            if "application/json" in content_type_:
                encoding_, onchain_data_ = remainder_.split(",", 1)
                if encoding_ == "utf8":
                    metadata_ = json.loads(onchain_data_)
                elif encoding_ == "base64":
                    encoded_data_ = base64.b64decode(onchain_data_)
                    decoded_data_ = encoded_data_.decode(encoding="utf-8")
                    metadata_ = json.loads(decoded_data_)
                else:
                    log.error(
                        'Unhandled encoding "%s" detected for %s', encoding_, token_uri_
                    )
                    metadata_ = {}
            else:
                log.error(
                    'Unhandled content-type "%s" detected for %s', content_type_, token_uri_
                )
                metadata_ = {}
        return metadata_

    data_url = token_uri.split(",", 1)[-1]
    parts = urlparse(data_url)
    if parts.scheme:
        if parts.scheme == "ipfs":
            metadata = _extract_metadata_from_ipfs(data_url)
        elif parts.scheme in ("http", "https"):
            metadata = _extract_metadata_from_public_internet_url(data_url)
        else:
            log.error(
                'Unhandled URL scheme "%s" detected for %s', parts.scheme, data_url
            )
            metadata = {}
    else:
        metadata = _extract_metadata_from_onchain(token_uri)
    return metadata


def resolve_addresses(*addresses):
    retval = set()
    for address in addresses:
        if web3.Web3.isAddress(address):
            retval.add(address)
        if retrieved_address := the_graph.query_ens_by_domain(address):
            retval.add(retrieved_address)
    return retval
