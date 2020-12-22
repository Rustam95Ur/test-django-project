from django.db import models


class LoginTime(models.Model):
    """ Модель статиски посещения"""
    sa_code = models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agents_login_time'
