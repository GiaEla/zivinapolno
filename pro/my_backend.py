from django.contrib.auth import get_user_model


class UserBackend(object):

    def get_user(self, user_id):
        usermodel = get_user_model()
        try:
            return usermodel.objects.get(pk=user_id)
        except usermodel.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(email=username)
        except usermodel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and  user.check_password(password):
                return user
        return None