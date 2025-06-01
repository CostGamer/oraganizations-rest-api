class AlreadyManyTokensError(Exception):
    pass


class UserHasNoTokensError(Exception):
    pass


class MissingOrBadTokenError(Exception):
    pass


class OrganizationNotFoundError(Exception):
    pass


class AddressNotFoundError(Exception):
    pass


class TheLimitExceededError(Exception):
    pass


class ActivityNotFoundError(Exception):
    pass
