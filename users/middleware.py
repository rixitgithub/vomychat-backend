from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ['/login/', '/register/']:
            return

        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(access_token)
                request.user = jwt_auth.get_user(validated_token)
                # No need to manually set is_authenticated; Django handles this.
            except InvalidToken:
                request.user = None
