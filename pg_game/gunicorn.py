from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '0.0.0.0:' + environ.get('PORT', '8005')
worker = 4

env = {
    'DJANGO_SETTINGS_MODULE': 'pg_game.settings'
}

reload = True
name = 'pg_game'
