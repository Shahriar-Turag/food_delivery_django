from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomTokenAuthentication(BaseAuthentication):
  keyword = 'token'
  
  def authenticate(self, request):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return None
    
    try:
      keyword, token = auth.split()
    except ValueError:
      raise AuthenticationFailed('Invalid token header. No credentials provided.')
    
    if keyword.lower() != self.keyword:
      return None
    
    jwt.authenticator = JWTAuthentication()

    try:
      validated_token = jwt.authenticator.get_validated_token(token)
      return jwt.authenticator.get_user(validated_token), validated_token
    except Exception as e:
      raise AuthenticationFailed('Invalid token')