from rest_framework import permissions
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from tokens.models import Token


class SafeSessionTokenAuthentication(SessionAuthentication):
    """
    Authentication backend for doing GET requests.
    It will look if the given token exists, user needs
    to be logged in.
    """
    def authenticate(self, request):
        if request.method != 'GET':
            return None
        key = request.query_params.get('key', None)
        if not Token.objects.filter(key=key).exists():
            return None
        return super().authenticate(request)


class SafeTokenAuthentication(BaseAuthentication):
    """
    Authentication backend for doing GET requests.
    It will look if the given token exists, user does NOT
    need to be logged in.
    """
    def authenticate(self, request):
        if request.method != 'GET':
            return None
        key = request.query_params.get('key', None)

        if not key:
            return None

        try:
            user = Token.objects.get(key=key).user
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Could not find the token: %s' % key)

        return (user, None)


class UnsafeJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    """
    Authentication backend for doing POST, PUT, DELETE requests.
    It will call the JSONWebTokenAuthentication parent authenticate
    method.
    """
    def authenticate(self, request):
        if request.method not in ['POST', 'PUT', 'DELETE']:
            return None
        return super().authenticate(request)


class IsOwner(BasePermission):
    """
    Permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request with an valid key.
        key = request.query_params.get('key', None)

        if request.method in permissions.SAFE_METHODS and Token.objects.filter(key=key).exists():
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user