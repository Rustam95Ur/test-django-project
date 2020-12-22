from django.db import models


class GroupSetting(models.Model):
    """ Модель для группы настроек """
    title = models.CharField(max_length=225, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Статус')

    def __str__(self):
        return 'id: %d, %s, %s' % (
            self.id, self.title, self.is_active)

    class Meta:
        db_table = 'upload_group_setting'


class UploadSetting(models.Model):
    """ Модель настроек"""
    TYPE_KPI = 1
    TYPE_PROGRESS = 2
    TYPE_VAL_STAR = 1
    TYPE_VAL_PERCENT = 2
    TYPE_VAL_DISPLAY = 3
    type_id = models.IntegerField(verbose_name='Тип настройки')
    title = models.CharField(max_length=100, verbose_name='Название', null=True)
    col_name = models.CharField(max_length=200, verbose_name='Название колоны', unique=True)
    type_val = models.CharField(max_length=100, verbose_name='Tип ранга', null=True)
    value = models.CharField(max_length=200, verbose_name='Значение', null=True)
    group = models.ForeignKey(GroupSetting, models.SET_NULL, blank=True, null=True, verbose_name='Связь с группой')

    def __str__(self):
        return 'id: %d, %s, %s, %s, %s' % (
            self.id, self.type_id, self.title, self.value, self.col_name)

    class Meta:
        db_table = 'upload_setting'
        verbose_name = 'Настройка'
