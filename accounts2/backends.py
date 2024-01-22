from django.contrib.auth.backends import ModelBackend
from .models import Account, Catedratico

class MultiModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, model=None, **kwargs):
        if model == 'Account':
            user = Account.objects.get(email=email)
        elif model == 'Catedratico':
            user = Catedratico.objects.get(email=email)
        else:
            return None  # Model no especificado o no reconocido

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            try:
                return Catedratico.objects.get(pk=user_id)
            except Catedratico.DoesNotExist:
                return None