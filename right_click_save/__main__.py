import click

from . import utils


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
def main(addresses):
    for token in utils.get_tokens(*addresses):
        click.echo(f'   {token.meta_data["name"]}')


if __name__ == "__main__":
    main()
