from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


UserModel = get_user_model()
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        ident = username.strip()

        users = list(
            UserModel.objects.filter(
                Q(username=ident) | Q(email__iexact=ident)
            )[:2]
        )

        if len(users) != 1:
            UserModel().set_password(password)
            return None

        user = users[0]
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None