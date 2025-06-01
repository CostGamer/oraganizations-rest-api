from http import HTTPStatus
from typing import Any


def create_error_responses(
    error_responses: dict[int, dict[str, dict[str, Any]]]
) -> dict:
    """Generates error response schemas for an API based on provided error examples.

    This function takes a dictionary of error status codes and their associated examples,
    then constructs a response schema for each status code in a format compatible with OpenAPI.

    Args:
        error_responses (dict[int, dict[str, dict[str, Any]]]): A dictionary where the keys are
                                                              HTTP status codes (integers) and the values
                                                              are dictionaries containing response examples
                                                              for each status code.

    Returns:
        dict: A dictionary of response schemas for each error status code, where the keys are status codes
              and the values are response descriptions and examples formatted for OpenAPI specification.
    """
    responses = {}

    for status_code, examples in error_responses.items():
        description = HTTPStatus(status_code).phrase
        responses[status_code] = {
            "description": description,
            "content": {"application/json": {"examples": examples}},
        }

    return responses


issue_token_exceptions = {
    400: {
        "many_tokens_error": {
            "summary": "AlreadyManyTokensError",
            "value": {
                "detail": "This user already has 5 tokens, use the /get_all_tokens endpoint to get all tokens"
            },
        },
    },
}

get_all_tokens_exceptions = {
    404: {
        "user_has_no_tokens_error": {
            "summary": "UserHasNoTokensError",
            "value": {
                "detail": "User has no tokens, use the /issue_token endpoint to issue a new token"
            },
        },
    },
}

get_organization_by_name_exceptions = {
    400: {
        "limit_exceed_error": {
            "summary": "TheLimitExceededError",
            "value": {"detail": "The limit of requests exceeded"},
        },
    },
    401: {
        "missing_or_bad_token": {
            "summary": "MissingOrBadTokenError",
            "value": {"detail": "The token is missing or bad"},
        },
    },
    404: {
        "organization_not_exists_error": {
            "summary": "OrganizationNotFoundError",
            "value": {"detail": "This organization does not exist"},
        },
    },
}

get_organizations_by_address_exceptions = {
    400: {
        "limit_exceed_error": {
            "summary": "TheLimitExceededError",
            "value": {"detail": "The limit of requests exceeded"},
        },
    },
    401: {
        "missing_or_bad_token": {
            "summary": "MissingOrBadTokenError",
            "value": {"detail": "The token is missing or bad"},
        },
    },
    404: {
        "address_not_exists_error": {
            "summary": "AddressNotFoundError",
            "value": {"detail": "This address does not exist"},
        },
        "organization_not_exists_error": {
            "summary": "OrganizationNotFoundError",
            "value": {"detail": "This organization does not exist"},
        },
    },
}

get_organizations_by_activity_exceptions = {
    400: {
        "limit_exceed_error": {
            "summary": "TheLimitExceededError",
            "value": {"detail": "The limit of requests exceeded"},
        },
    },
    401: {
        "missing_or_bad_token": {
            "summary": "MissingOrBadTokenError",
            "value": {"detail": "The token is missing or bad"},
        },
    },
    404: {
        "activity_not_exists_error": {
            "summary": "ActivityNotFoundError",
            "value": {"detail": "This activity does not exist"},
        },
        "organization_not_exists_error": {
            "summary": "OrganizationNotFoundError",
            "value": {"detail": "This organization does not exist"},
        },
    },
}

get_organization_by_id_geo_exceptions = {
    400: {
        "limit_exceed_error": {
            "summary": "TheLimitExceededError",
            "value": {"detail": "The limit of requests exceeded"},
        },
    },
    401: {
        "missing_or_bad_token": {
            "summary": "MissingOrBadTokenError",
            "value": {"detail": "The token is missing or bad"},
        },
    },
    404: {
        "organization_not_exists_error": {
            "summary": "OrganizationNotFoundError",
            "value": {"detail": "This organization does not exist"},
        },
    },
}


issue_token_responses = create_error_responses(issue_token_exceptions)
get_all_tokens_responses = create_error_responses(get_all_tokens_exceptions)
get_organization_by_name_responses = create_error_responses(
    get_organization_by_name_exceptions
)
get_organizations_by_address_responses = create_error_responses(
    get_organizations_by_address_exceptions
)
get_organizations_by_activity_responses = create_error_responses(
    get_organizations_by_activity_exceptions
)
get_organization_by_id_geo_responses = create_error_responses(
    get_organization_by_id_geo_exceptions
)
