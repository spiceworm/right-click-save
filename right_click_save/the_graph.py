import requests

from .exceptions import ENSLookupError, TheGraphQueryError


BASE_URL = "https://api.thegraph.com"
ENS_SUBGRAPH = "ensdomains/ens"
ERC721_SUBGRAPH = "amxx/eip721-subgraph"


def _query(q, subgraph):
    r = requests.post(
        f"{BASE_URL}/subgraphs/name/{subgraph}",
        json={"query": q},
    )
    r.raise_for_status()
    resp = r.json()
    if "errors" in resp:
        raise TheGraphQueryError(resp["errors"])
    return resp["data"]


def query_ens_by_domain(domain, subgraph=ENS_SUBGRAPH):
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


def query_ens_by_labelhash(labelhash, subgraph=ENS_SUBGRAPH):
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


def query_erc721(address, subgraph=ERC721_SUBGRAPH):
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
