from django.db import models
from pg_game.settings import EXCEL_DIRECTORY, AGENT_IMAGE_DIRECTORY


def content_file_name(instance, filename):
    """Путь хранения загрузки файлов"""
    return EXCEL_DIRECTORY + "{file}".format(folder=instance.id,
                                             file=filename)


def agent_directory_path(instance, filename):
    """Путь хранения картинок агентов"""
    ext = filename.split('.')[-1]
    file = instance.code + '.' + ext

    return AGENT_IMAGE_DIRECTORY + '{0}'.format(file)


class UploadHistory(models.Model):
    """ Модель истрории сохранения файла"""
    user_info = models.CharField(max_length=100, verbose_name='Ф.И.О')
    file_name = models.CharField(max_length=100, verbose_name='Название файла')
    file_path = models.FileField(upload_to=content_file_name, verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата создание')

    class Meta:
        db_table = 'upload_history'


class History(models.Model):
    """ Модель истории торгового представителя  """
    sa_code = models.CharField(max_length=20, verbose_name='SA код')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О')
    kpi_val = models.TextField(verbose_name='Значение КPI')
    kpi_key = models.TextField(verbose_name='Ключ KPI')
    progress_val = models.TextField(verbose_name='Значения прогресса')
    progress_key = models.TextField(verbose_name='Ключ прогресса')
    branch_name = models.CharField(max_length=100, verbose_name='Подразделение')
    sort_id = models.IntegerField(null=True, verbose_name='Сортировка')
    is_authenticated = models.BooleanField(default=True)

    def __str__(self):
        return 'id: %d, %s, %s , %s , %s , %s' % (
            self.id, self.sa_code, self.full_name, self.branch_name, self.sort_id, self.full_name)

    class Meta:
        db_table = 'agents_history'


class AgentImage(models.Model):
    """ Модель фотографий торгового представителя  """
    code = models.CharField(max_length=20, verbose_name='Код ТП')
    image = models.ImageField(upload_to=agent_directory_path, default='images/icons/default_logo.png',
                              verbose_name='Фото агента', null=True)

    class Meta:
        db_table = 'agents_images'
