class RightClickSaveError(Exception):
    pass


class TheGraphQueryError(RightClickSaveError):
    pass


class ENSLookupError(TheGraphQueryError):
    pass
