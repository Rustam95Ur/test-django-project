from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from .models import UploadSetting, GroupSetting
from .forms import SettingUpdateForm, GroupUpdateForm
from pg_game.settings import VALIDATE


@login_required(login_url='login')
def settings_list(request):
    """ Списко настроек """
    settings_obj = UploadSetting.objects.select_related('group').all()
    groups_obj = GroupSetting.objects.filter(is_active=True)
    data = {'settings': settings_obj, 'groups': groups_obj}
    return render(request, 'setting/list.html', context=data)


@login_required(login_url='login')
def save_or_update(request):
    """ Сохранение/обновление записи настройки"""
    if request.POST:
        type_id = int(request.POST.get('type_id'))
        setting_group = request.POST.get('group')
        if request.POST.get('id') is None or request.POST.get('id') == '':
            upload_setting_obj = UploadSetting.objects.filter(group_id=setting_group)
            form = SettingUpdateForm(request.POST)
            status_message = 'Настройка успешно создана'
            if type_id == 1 and len(setting_group) > 0:
                if len(upload_setting_obj) >= 3:
                    messages.add_message(request, messages.ERROR, 'Максимальное настроек в одной группе равна 3')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                for setting in upload_setting_obj:
                    if setting.type_val == request.POST.get('type_val'):
                        messages.add_message(request, messages.ERROR, 'Такой тип колонки существует')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            settings_obj = get_object_or_404(UploadSetting, id=request.POST.get('id'))
            form = SettingUpdateForm(request.POST, instance=settings_obj)
            status_message = 'Настройка успешно обновлена'

            upload_setting_obj = UploadSetting.objects.filter(group_id=setting_group,
                                                              type_val=request.POST.get('type_val')).first()
            if int(request.POST.get('change_type_val')) == 1 and upload_setting_obj:
                messages.add_message(request, messages.ERROR, 'Такой тип колонки существует')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, status_message)
        else:
            messages.add_message(request, VALIDATE, form.errors, extra_tags='validate')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def setting_delete(request, setting_id):
    """ Удаление настройки через ajax"""
    setting_obj = get_object_or_404(UploadSetting, id=setting_id)
    setting_obj.delete()
    return JsonResponse({'message': 'Настройка успешна удалена', 'title': 'Успешно', 'status': 'success'}, status=200)


@login_required(login_url='login')
def setting_groups_list(request):
    """ Списко настроек """
    groups_obj = GroupSetting.objects.all()
    data = {'groups': groups_obj}
    return render(request, 'setting/group_list.html', context=data)


@login_required(login_url='login')
def setting_groups_save(request):
    """ Сохрание/Обновления группы """
    if request.POST:
        if request.POST.get('id') is None or request.POST.get('id') == '':
            form = GroupUpdateForm(request.POST, request.FILES)
            status_message = 'Группа успешно создана'
        else:
            rank = get_object_or_404(GroupSetting, id=request.POST.get('id'))
            form = GroupUpdateForm(request.POST, instance=rank)
            status_message = 'Группа успешно обновлена'
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, status_message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.add_message(request, VALIDATE, form.errors, extra_tags='validate')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def setting_groups_delete(request, group_id):
    """ Удаление настройки через ajax"""
    group_obj = get_object_or_404(GroupSetting, id=group_id)
    group_settings = group_obj.uploadsetting_set.count()
    if group_settings > 0:
        return JsonResponse(
            {'message': 'Нельзя удалить группу, так как у нее зависимости', 'title': 'Ошибка', 'status': 'error'},
            status=400)
    else:
        group_obj.delete()
        return JsonResponse({'message': 'Группа успешна удалена', 'title': 'Успешно', 'status': 'success'}, status=200)
