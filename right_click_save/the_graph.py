import requests

from .constants import subgraphs
from .exceptions import ENSLookupError, TheGraphQueryError


def _query(q, subgraph):
    r = requests.post(
        f"{subgraphs.BASE_URL}/subgraphs/name/{subgraph}",
        json={"query": q},
    )
    r.raise_for_status()
    resp = r.json()
    if "errors" in resp:
        raise TheGraphQueryError(resp["errors"])
    return resp["data"]


def query_decentraland_by_token_id(token_id, subgraph=subgraphs.DECENTRALAND):
    q = f"""
    {{
      nfts(where: {{tokenId: "{token_id}"}}) {{
        name
      }}
    }}
    """
    try:
        data = _query(q, subgraph)
    except TheGraphQueryError as e:
        raise ENSLookupError(e)
    else:
        if domains := data["nfts"]:
            return domains[0]["name"]
        return None


def query_ens_by_domain(domain, subgraph=subgraphs.ENS):
    q = f"""
    {{
      domains(where: {{name: "{domain}"}}) {{
        owner {{
          id
        }}
      }}
    }}
    """
    try:
        data = _query(q, subgraph)
    except TheGraphQueryError as e:
        raise ENSLookupError(e)
    else:
        if domains := data["domains"]:
            return domains[0]["owner"]["id"]
        return None


def query_ens_by_labelhash(labelhash, subgraph=subgraphs.ENS):
    q = f"""
    {{
      domains(where: {{labelhash: "{labelhash}"}}) {{
        name
      }}
    }}
    """
    try:
        data = _query(q, subgraph)
    except TheGraphQueryError as e:
        raise ENSLookupError(e)
    else:
        if domains := data["domains"]:
            return domains[0]["name"]
        return None


def query_erc721(address, subgraph=subgraphs.ERC721):
    q = f"""
    {{
      accounts(where: {{id: "{address}"}}) {{
        tokens {{
          id
          uri
        }}
      }}
    }}
    """
    try:
        return _query(q, subgraph)
    except TheGraphQueryError as e:
        raise ENSLookupError(e)
