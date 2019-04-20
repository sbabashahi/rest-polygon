import coreapi
from rest_framework.schemas import AutoSchema


def jwt_response_payload_handler(token, user):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}). data
        }

    """
    return {
        'token': token,
        'user': {
            'phone_number': user.profile.phone_number,
            'email': user.email,
            'name': user.profile.name,
            'language': user.profile.language,
            'currency': user.profile.currency,
        },
    }


def jwt_get_secret_key(user):
    """
    Use this in generating and checking JWT token,
    and when logout jwt_secret will change so previous JWT token wil be invalidate
    :param user:
    :return:
    """
    return user.profile.jwt_secret


CUSTOM_PAGINATION_SCHEMA = AutoSchema(manual_fields=[
    coreapi.Field("index", required=False, location="query", type="integer", description="pagination index"),
    coreapi.Field("size", required=False, location="query", type="integer", description="pagination size"),
    coreapi.Field("order_by", required=False, location="query", type="string", description="sort list"),
])
