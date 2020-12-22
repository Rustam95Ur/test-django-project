from django.db import models


class ErrorAuthList(models.Model):
    date = models.DateTimeField(verbose_name="Дата попытка")
    login = models.CharField(max_length=50, verbose_name="Логи")
    ip = models.CharField(max_length=50, verbose_name="IP адрес")
    text = models.CharField(max_length=100, verbose_name="Текст ошибки")

    def get_title():
        return "История попыток входа"

    def isreadonly():
        return True

    def __str__(self):
        return 'id: %d, %s, %s' % (self.id, self.login, self.text)

    class Meta:
        db_table = 'auth_error_list'
