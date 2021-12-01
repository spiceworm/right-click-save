import requests


BASE_URL = "https://api.thegraph.com"


def _query(q, subgraph):
    r = requests.post(
        f"{BASE_URL}/subgraphs/name/{subgraph}",
        json={"query": q},
    )
    r.raise_for_status()
    resp = r.json()
    if "errors" in resp:
        raise Exception(resp["errors"])
    return resp["data"]


def query_ens(domain, subgraph="ensdomains/ens"):
    q = f"""
    {{
      domains(where: {{name: "{domain}"}}) {{
        owner {{
          id
        }}
      }}
    }}
    """
    data = _query(q, subgraph)
    if domains := data["domains"]:
        return domains[0]["owner"]["id"]
    return None


def query_erc721(address, subgraph="amxx/eip721-subgraph"):
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
    return _query(q, subgraph)
