from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from django.utils import timezone
from users.models import ErrorAuthList
import radius

UserModel = get_user_model()


class ModelBackendLdap(ModelBackend):
    # ACD++ изменена данная функция по отношению    к классу родителю
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        # ACD++ Проверка на то что логин написан с указанием домена
        if '@' in username:
            username = username.split('@')[0]
        if '\\' in username:
            username = username.split('\\')[1]
        if '/' in username:
            username = username.split('/')[1]
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
            ErrorAuthList(
                date=timezone.now(),
                login=username,
                ip=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
                text='Не определен пользователь'
            ).save()
        else:
            # ACD++ заменена вызываемая функция, теперь здесь выполняется попытка присоеденится к AD
            # по протоколу RADIUS

            if not self.user_can_authenticate(user):
                ErrorAuthList(
                    date=timezone.now(),
                    login=username,
                    ip=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
                    text='Пользователь заблокирован'
                ).save()
            elif not check_username_and_password_by_radius(username, password, request):
                ErrorAuthList(
                    date=timezone.now(),
                    login=username,
                    ip=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
                    text='Не верный пароль'
                ).save()
            else:
                return user


def check_username_and_password_by_radius(username, password, request):
    # ACD++ в этой функции выполняется проверка через RADIUS
    if settings.RADIUS_DISABLE:
        return True
    try:
        r = radius.Radius(settings.RADIUS_SECRET, host=settings.RADIUS_HOST, port=settings.RADIUS_PORT)
        return r.authenticate(username, password)
        pass
    except Exception as e:
        ErrorAuthList(
            date=timezone.now(),
            login=username,
            ip=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
            text='Ошибка проверки авторизации: %s' % e.__class__
        ).save()
        pass
    return False


class RemoteUserBackendNonCreateUnknownUser(RemoteUserBackend):
    # ACD++ не создавать пользователей которые есть в AD, но отсутствуют в базе портала
    create_unknown_user = False
