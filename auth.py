import json
import os
from flask import (
    request,
    _request_ctx_stack,
    abort
)
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    # get the header from the request
    auth = request.headers.get('Authorization', None)

    # raise an AuthError if no header is present
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # tsplit bearer and the token
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    # check if the header is malformed
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # return the token part of the header
    token = parts[1]
    return token


def check_permissions(permission, payload):
    '''
    @INPUTS
        permission: string permission (i.e. 'post:recipe')
        payload: decoded jwt payload
    '''
    # if permissions are not included in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)

    # if the requested permission string is not in the payload permissions
    # array
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


def verify_decode_jwt(token):

    # get the public key from Auth0
    # verify the token using Auth0 /.well-known/jwks.json
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        print('not kid')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
        # use the key to validate the jwt
    if rsa_key:
        try:
            # decode the payload from the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, \
                                check the audience and issuer.'
            }, 401)
        except Exception:
            print('5')
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    '''
    @INPUTS
        permission: string permission (i.e. 'post:recipe')
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get the token
            token = get_token_auth_header()
            try:
                # to decode the jwt
                payload = verify_decode_jwt(token)
            except BaseException:
                print('10')
                abort(401)
            # validate claims and check the requested permission
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
