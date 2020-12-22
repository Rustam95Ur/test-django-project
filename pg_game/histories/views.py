from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from histories.models import UploadHistory, History, AgentImage
from settings.models import UploadSetting
from django.shortcuts import get_object_or_404
from pg_game.upload_settings import MAIN_COLUMNS, BOOK_NAME, VALIDATE, COLOR_GREEN, COLOR_RED, COLOR_YELLOW
from .forms import ImageUpdateForm
import json
import openpyxl


@login_required(login_url='login')
def history_page(request):
    """ Страница загрузки файла """
    upload_histories_obj = UploadHistory.objects.all()
    data = {'histories': upload_histories_obj}
    return render(request, 'history/index.html', context=data)


@login_required(login_url='login')
def history_file_upload(request):
    """ Загрузка файла в сессию """
    if request.POST:
        if 'excel_file_data' in request.session:
            del request.session['excel_file_data']
        main_settings = MAIN_COLUMNS
        if len(main_settings) != 3:
            return JsonResponse({'message': 'Отсутствует основные настройки. Обратитесь администратору'}, status=400)

        excel_file = request.FILES["file"]
        wb = openpyxl.load_workbook(excel_file)
        if str(BOOK_NAME) != str(wb.worksheets[0].title) or len(wb.worksheets) > 1:
            return JsonResponse({'message': 'Ошибки в название книги. Проверьте файл'}, status=400)
        worksheet = wb[BOOK_NAME]
        excel_headers_list = []
        excel_data_list = []
        kpi_settings_list = []
        progress_settings_list = []

        admin_settings_obj = UploadSetting.objects.all()

        # получение название настроек
        for setting in admin_settings_obj:
            if int(setting.type_id) == UploadSetting.TYPE_KPI:
                if setting.group.is_active:
                    kpi_settings_list.append(setting.col_name)
            if int(setting.type_id) == UploadSetting.TYPE_PROGRESS:
                progress_settings_list.append(setting.col_name)
                progress_settings_list.append(setting.value)
        counter = 0
        # получение заголовков и данных в виде двух списков
        for row in worksheet.iter_rows():
            row_data = []
            if counter == 0:
                for cell in row:
                    excel_headers_list.append(cell.value)
            else:
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data_list.append(row_data)
            counter += 1

        for main in main_settings:
            if main not in excel_headers_list:
                return JsonResponse({'message': 'Отсутствует основные настройки в excel-e. Проверьте файл'}, status=400)
        main_index_list = []
        # получение индексов основных данных
        for s_key, main in enumerate(main_settings):
            for e_key, header in enumerate(excel_headers_list):
                if header == main:
                    main_index_list.append(e_key)

        kpi_index_list = []
        kpi_key_list = []
        # получение индексов kpi
        for e_key, header in enumerate(excel_headers_list):
            for a_key, admin in enumerate(kpi_settings_list):
                if header == admin:
                    kpi_key_list.append(header)
                    kpi_index_list.append(e_key)
        progress_index_list = []
        progress_key_list = []
        # получение индексов достижений
        for a_key, admin in enumerate(progress_settings_list):
            for e_key, header in enumerate(excel_headers_list):
                if header == admin:
                    progress_key_list.append(header)
                    progress_index_list.append(e_key)
        kpi_data = get_date_in_excel(excel_data_list, kpi_index_list)
        progress_data_list = get_date_in_excel(excel_data_list, progress_index_list)
        result_data = get_date_in_excel(excel_data_list, main_index_list)
        for key, value in enumerate(result_data):
            if kpi_data and kpi_data[key]:
                value.append(kpi_data[key])
            else:
                value.append(None)
            if kpi_key_list:
                value.append(kpi_key_list)
            else:
                value.append(None)
            if progress_data_list and progress_data_list[key]:
                value.append(progress_data_list[key])
            else:
                value.append(None)
            if progress_key_list:
                value.append(progress_key_list)
            else:
                value.append(None)
        excel_data = json.dumps(result_data)
        excel_headers = json.dumps(excel_headers_list)
        request.session['excel_file_data'] = excel_data
        request.session['excel_headers'] = excel_headers
        return JsonResponse({'message': 'Данные верны'}, status=200)
    else:
        return JsonResponse({'message': 'Unsupported method get'}, status=400)


@login_required(login_url='login')
def history_file_save(request):
    """ Сохранение данных в базу"""
    if request.POST:
        if 'excel_file_data' not in request.session:
            error_message = 'Данные файла отсуствуют'
            return JsonResponse({'message': error_message}, status=400)
        user = request.user
        upload_save = UploadHistory(user_info=user.last_name + ' ' + user.first_name, file_name=request.FILES["file"],
                                    file_path=request.FILES["file"])
        History.objects.all().delete()
        sort = 1
        result_data = json.loads(request.session['excel_file_data'])
        excel_headers_list = json.loads(request.session['excel_headers'])
        for data in result_data:
            check_history = History.objects.filter(sa_code=data[excel_headers_list.index('SA_code')]).exists()
            if not check_history:
                save_history = History(branch_name=data[excel_headers_list.index('Branch_Name')],
                                       sa_code=data[excel_headers_list.index('SA_code')].lower(),
                                       full_name=data[excel_headers_list.index('SA_Name')],
                                       kpi_val=json.dumps(data[3]), kpi_key=json.dumps(data[4]),
                                       progress_val=json.dumps(data[5]), progress_key=json.dumps(data[6]),
                                       sort_id=sort)
                save_history.save()
                sort += 1
            else:
                error_message = 'У вас дублирующий SA код {} в файле. Исправьте или удалите запись'.format(
                    data[excel_headers_list.index('SA_code')])
                return JsonResponse({'message': error_message, 'title': 'Ошибка', 'status': 'error'}, status=200)
        upload_save.save()
        return JsonResponse({'message': 'Данные успешно сохранены', 'title': 'Успешно', 'status': 'success'},
                            status=200)
    else:
        return JsonResponse({'message': 'Неподдерживаемый метод get', 'title': 'Ошибка', 'status': 'error'}, status=400)


@login_required(login_url='login')
def agents_history(request):
    """ Страница списков ТП файла """
    histories_obj = History.objects.all()
    data = {'histories': histories_obj}
    return render(request, 'history/agents_list.html', context=data)


@login_required(login_url='login')
def agent_history(request, agent_id):
    """ Страница информаци о ТП """
    agent_history_obj = get_object_or_404(History, id=agent_id)
    agent_image_obj = AgentImage.objects.filter(code=agent_history_obj.sa_code).first()
    admin_settings_obj = UploadSetting.objects.all()
    kpi_val_list = json.loads(agent_history_obj.kpi_val)
    progress_val_list = json.loads(agent_history_obj.progress_val)
    kpi_settings_list = json.loads(agent_history_obj.kpi_key)
    progress_setting_list = json.loads(agent_history_obj.progress_key)
    progress_data_list = []
    group_list = []
    for setting in admin_settings_obj:
        if progress_setting_list and setting.col_name in progress_setting_list:
            progress_dict = {'title': setting.title,
                             'current_val': progress_val_list[progress_setting_list.index(setting.value)],
                             'user_val': progress_val_list[progress_setting_list.index(setting.col_name)]}
            progress_data_list.append(progress_dict)
        if kpi_settings_list and setting.col_name in kpi_settings_list:
            if setting.group.is_active:
                group_list.append(setting.group_id)
    star = 0
    percent = 0
    display = 1
    kpi_data_list = []
    kpi_dict = {}
    color = None
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
                    if percent > 100:
                        color = COLOR_GREEN
                    elif percent < 90:
                        color = COLOR_RED
                    elif percent >= 90 and percent < 100:
                        color = COLOR_YELLOW
                    kpi_dict = {'title': setting.group.title, 'star': star, 'percent': percent, 'color': color,
                                'show': display}
        kpi_data_list.append(kpi_dict)
    data = {'kpi_values': kpi_data_list, 'progress': progress_data_list, 'agent_image': agent_image_obj,
            'history': agent_history_obj}
    return render(request, 'history/agent_view.html', context=data)


@login_required(login_url='login')
def agent_update_image(request):
    """ Страница информаци о ТП """
    if request.POST:
        get_object_or_404(History, sa_code=request.POST.get('code'))
        form = ImageUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Картинка обновлена')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.add_message(request, VALIDATE, form.errors, extra_tags='validate')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def get_date_in_excel(data_list, index_list):
    result_list = []
    for values in data_list:
        excel_list = []
        for key, value in enumerate(values):
            if key in index_list:
                if value != 'None':
                    excel_list.append(value)
        if excel_list:
            result_list.append(excel_list)
    return result_list
