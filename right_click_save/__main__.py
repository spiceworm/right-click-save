import logging

import click

from . import utils


log = logging.getLogger(__name__)


class EthereumAddress(click.types.StringParamType):
    name = "ethereum-address"

    def convert(self, value, param, ctx):
        address_or_ens_domain = super().convert(value, param, ctx)
        if retval := utils.resolve_addresses(address_or_ens_domain):
            return retval.pop()
        self.fail(f'Invalid ethereum address "{value}"', param, ctx)

    def __repr__(self):
        return "ETHEREUM ADDRESS"


@click.command()
@click.argument("addresses", required=True, nargs=-1, type=EthereumAddress())
@click.option("-v", "--verbose", is_flag=True)
def main(addresses, verbose):
    if verbose:
        logging.basicConfig()
    else:
        logging.disable(logging.CRITICAL)

    for token in utils.get_tokens(*addresses):
        if token_project_name := token.metadata.get("name"):
            click.echo(f"   {token_project_name}")


if __name__ == "__main__":
    main()
