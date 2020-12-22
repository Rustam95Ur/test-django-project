FROM registry.applecity.kz/python/alpine-3.7:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/pg_game

COPY pg_game /var/www/pg_game

#RUN echo http://mirror.yandex.ru/mirrors/alpine/v3.10/main > /etc/apk/repositories; \
#    echo http://mirror.yandex.ru/mirrors/alpine/v3.10/community >> /etc/apk/repositories

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

RUN apk del .build-deps

EXPOSE 8009

CMD ["python", "manage.py", "runserver", "0.0.0.0:8009"]
