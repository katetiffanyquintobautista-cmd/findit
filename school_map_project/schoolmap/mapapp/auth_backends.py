from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """Allow authentication with either email or username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None

        candidates = UserModel.objects.filter(
            Q(email__iexact=username) | Q(username__iexact=username)
        )

        for user in candidates:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
