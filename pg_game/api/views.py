from rest_framework.response import Response
from rest_framework import decorators, permissions, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from os import listdir
from .serializers import AgentImageSerializer
from histories.models import AgentImage, History
from pg_game import upload_settings
from pg_game.settings import APK_DIRECTORY, BETA_TESTERS
from settings.models import UploadSetting, GroupSetting
import json

token = openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, required=True)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Профиль',
    operation_description='Получения информаций',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_profile(request):
    """ Получения профиля пользователя"""
    agent = request.user
    agent_profile_dict = {'full_name': agent.full_name, 'route': agent.sa_code, 'subdivision': agent.branch_name}
    return Response(agent_profile_dict, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    manual_parameters=[token],
    responses={
        201: 'Данные успешно сохранены',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE, description='Картинка', required=['image']),
        },
    ),
    security=[],
    operation_id='Обновления профиля',
    operation_description='Обновления профилья пользователя',
)
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """ Сохранение картинок для анкеты """
    image = request.data['image']
    agent = request.user
    serializer_data = {'code': agent.sa_code, 'image': image}
    agent_image_obj = AgentImage.objects.filter(code=agent.sa_code).first()
    images_serializer = AgentImageSerializer(data=serializer_data, instance=agent_image_obj or None)
    if images_serializer.is_valid(raise_exception=True):
        images_serializer.save()
    result = {'status': 'success', 'message': 'Данные успешно обновлены'}
    return Response(result, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Статистика профиля',
    operation_description='Статистика профиля',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def profile_statistic(request):
    """Получения информаци о достижений и kpi пользователя"""
    agent = request.user
    check_history = History.objects.filter(sa_code=agent.sa_code).first()
    progress_data_list = []
    group_list = []
    kpi_data_list = []
    admin_settings_obj = UploadSetting.objects.all()
    kpi_val_list = json.loads(check_history.kpi_val)
    progress_val_list = json.loads(check_history.progress_val)
    kpi_settings_list = json.loads(check_history.kpi_key)
    progress_setting_list = json.loads(check_history.progress_key)

    for setting in admin_settings_obj:
        if setting.col_name in progress_setting_list:
            progress_dict = {'title': setting.title,
                             'user_val': int(progress_val_list[progress_setting_list.index(setting.col_name)]),
                             'current_val': int(progress_val_list[progress_setting_list.index(setting.value)])}
            progress_data_list.append(progress_dict)
        if setting.col_name in kpi_settings_list:
            if setting.group.is_active:
                group_list.append(setting.group_id)

    star = 0
    percent = 0
    color = None
    display = 1
    kpi_dict = {}
    group_list = list(set(group_list))
    for i in range(0, len(group_list)):
        for setting in admin_settings_obj:
            if setting.col_name in kpi_settings_list:
                if setting.group_id == group_list[i]:
                    if int(setting.type_val) == UploadSetting.TYPE_VAL_STAR:
                        star = kpi_val_list[kpi_settings_list.index(setting.col_name)]
                    elif int(setting.type_val) == UploadSetting.TYPE_VAL_PERCENT:
                        percent = int(float(kpi_val_list[kpi_settings_list.index(setting.col_name)]) * 100)
                    elif int(setting.type_val) == UploadSetting.TYPE_VAL_DISPLAY:
                        display = int(kpi_val_list[kpi_settings_list.index(setting.col_name)])
                    if percent >= 100:
                        color = upload_settings.COLOR_GREEN
                    elif percent <= 89:
                        color = upload_settings.COLOR_RED
                    elif percent >= 90 and percent < 100:
                        color = upload_settings.COLOR_YELLOW
                    kpi_dict = {'id': setting.group_id, 'title': setting.group.title,
                                'color': color, 'star': float(star), 'percent': percent, 'show': display}
        kpi_data_list.append(kpi_dict)
    current_user_dict = {'full_name': agent.full_name, 'route': agent.sa_code}
    data = {'current_user': current_user_dict, 'kpi': kpi_data_list,
            'progress': progress_data_list, }
    return Response(data)


count_path = openapi.Parameter('count', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, minimum=1)
page_path = openapi.Parameter('page', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, minimum=1)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token, count_path, page_path],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Рейтинги',
    operation_description='Рейтинг пользователей',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_ratings(request, count=10, page=1):
    """ Рейтинг пользователей"""
    if count == 0:
        return Response({'status': 'error', 'message': 'Incorrect number'})
    else:
        agent = request.user
        history_obj = History.objects.order_by('sort_id')
        paginator = Paginator(history_obj, count)
        page_obj = paginator.get_page(page)
        page_count = paginator.num_pages
        rating_list = []
        for history in page_obj:
            user_status = False
            image = '/media/images/icons/default_logo.png'
            if agent.sa_code == history.sa_code:
                user_status = True
                image_obj = AgentImage.objects.filter(code=agent.sa_code).first()
                image = image_obj.image.url
            rating_dict = {
                'user': {'full_name': history.full_name, 'image': image, 'current_user': user_status}}
            if rating_dict:
                rating_list.append(rating_dict)
        data = {'page_count': page_count, 'ratings': rating_list}
        return Response(data)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token, count_path, page_path],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Рейтинг',
    operation_description='Рейтинг по опрееделенному kpi',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_rating_by_id(request, kpi_id, count=10, page=0):
    """Рейтинг пользователи определенного kpi"""
    if count == 0:
        return Response({'status': 'error', 'message': 'Incorrect number'})
    else:
        kpi_group = get_object_or_404(GroupSetting, id=kpi_id)
        history_obj = History.objects.all()
        upload_setting_obj = UploadSetting.objects.select_related('group').filter(group_id=kpi_id)
        current_user_dict = {}
        rating_list = []
        kpi_title = kpi_group.title
        star = 0
        percent = 0
        user_value = 0
        kpi_percent_val = 0
        current_place = 0
        agent = request.user
        for history in history_obj:
            user_status = False
            image = '/media/images/icons/default_logo.png'
            if agent.sa_code == history.sa_code:
                image_obj = AgentImage.objects.filter(code=agent.sa_code).first()
                image = image_obj.image.url
                user_status = True
            for setting in upload_setting_obj:
                kpi_val_list = json.loads(history.kpi_val)
                kpi_key_list = json.loads(history.kpi_key)
                if setting.col_name in kpi_key_list:
                    if agent.sa_code == history.sa_code:
                        if int(setting.type_val) == UploadSetting.TYPE_VAL_STAR:
                            star = kpi_val_list[kpi_key_list.index(setting.col_name)]
                        elif int(setting.type_val) == UploadSetting.TYPE_VAL_PERCENT:
                            percent = int(float(kpi_val_list[kpi_key_list.index(setting.col_name)]) * 100)
                    if int(setting.type_val) == UploadSetting.TYPE_VAL_PERCENT:
                        kpi_percent_val = setting.col_name
                    if kpi_percent_val != 0:
                        user_value = int(float(kpi_val_list[kpi_key_list.index(kpi_percent_val)]) * 100)
            if agent.sa_code == history.sa_code:
                current_user_dict = {
                    'place': current_place,
                    'user': {'full_name': history.full_name, 'image': image}}
            rating_dict = {
                'user_val': user_value,
                'user': {'full_name': history.full_name, 'image': image,
                         'current_user': user_status}}
            if rating_dict:
                rating_list.append(rating_dict)
        rating_list.sort(key=lambda x: x['user_val'], reverse=True)
        place = 0
        count_list = 1
        for rating in rating_list:
            if rating['user']['current_user']:
                place = count_list
            count_list += 1
        current_user_dict['place'] = place
        page_count = round(len(rating_list) / count)
        page_start = (page - 1) * count
        page_stop = count * page
        data = {'page_count': page_count, 'current_user': current_user_dict,
                'current_kpi': {'title': kpi_title, 'star': star, 'percent': percent},
                'users_list': rating_list[page_start:page_stop]}
        return Response(data)


version_type_query = openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token, version_type_query],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Проверка версии',
    operation_description='Проверки версии приложения',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def check_version(request):
    version_type_type = request.GET.get('type')
    user_type = 'release'
    route = request.user.sa_code
    if version_type_type == 'debug':
        user_type = 'debug'
    if route.lower() in BETA_TESTERS:
        user_type = 'beta'
    if check_files_exists():
        response = {'user_type': user_type, "version": get_last_apk_version(user_type)}
    else:
        response = {'error': 'Отсутствуют файлы обновления на сервере'}
    return Response(response)


apk_type_path = openapi.Parameter('type_apk', openapi.IN_PATH, type=openapi.TYPE_STRING, required=True)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token, apk_type_path],
    responses={
        200: 'Запрос выполнен успешно',
        403: 'Неверный токен',
        400: 'Неверный формат запроса',
        404: 'Устроиство не найдено',
    },
    security=[],
    operation_id='Получить приложение',
    operation_description='Возврат файла',
)
@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_apk(request, type_apk):
    route = request.user.sa_code
    user_type = 'release'
    if type_apk == 'debug':
        user_type = type_apk
    if route.lower() in BETA_TESTERS:
        user_type = 'beta'
    if check_files_exists():
        filename = get_apk_filename(user_type)
        filepath = APK_DIRECTORY + filename
        response = FileResponse(open(filepath, 'rb'))
        return response
    else:
        response = {'error': 'Отсутствуют файлы обновления на сервере'}
        return Response(response)


def get_last_apk_version(get_type):
    """ Возраврат версии"""
    filename = get_apk_filename(get_type)
    parts_of_filename = filename.split('-')
    version = parts_of_filename[1].replace('.', '')
    return version


def get_apk_filename(get_type):
    """ Возврат название файла по типу"""
    content = listdir(APK_DIRECTORY)
    for filename in content:
        if get_type in filename:
            return filename
    return content[1]


def check_files_exists():
    """ Проверка наличий файла в папке"""
    content = listdir(APK_DIRECTORY)
    if content:
        return True
    else:
        return False
