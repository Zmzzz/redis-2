from  rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from  api import  models
class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        token_obj=models.Token.objects.filter(token=token).first()
        if not token_obj:
            raise AuthenticationFailed({'code':1002,'error':'认证失败'})
        return (token_obj.user,token_obj)
