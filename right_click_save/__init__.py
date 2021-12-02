from .__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from . import utils
from .token import Token


def get(*addresses_or_ens_domains):
    addresses = utils.resolve_addresses(*addresses_or_ens_domains)
    yield from utils.get_tokens(*addresses)
