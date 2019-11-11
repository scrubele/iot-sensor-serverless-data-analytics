from rest_framework.authentication import TokenAuthentication
from api.models import CustomAuthenticationToken

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = CustomAuthenticationToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('company').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.company.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.company, token