from right_click_save import the_graph


BLACKHOLE_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_query_ens_resolvable(requests_mock):
    requests_mock.post(
        f"{the_graph.BASE_URL}/subgraphs/name/{the_graph.ENS_SUBGRAPH}",
        json={"data": {"domains": [{"owner": {"id": BLACKHOLE_ADDRESS}}]}},
    )
    domain_owner = the_graph.query_ens("resolvable-domain.eth")
    assert domain_owner == BLACKHOLE_ADDRESS


def test_query_ens_unresolvable(requests_mock):
    requests_mock.post(
        f"{the_graph.BASE_URL}/subgraphs/name/{the_graph.ENS_SUBGRAPH}",
        json={"data": {"domains": []}},
    )
    domain_owner = the_graph.query_ens("unresolvable-domain.eth")
    assert domain_owner is None
