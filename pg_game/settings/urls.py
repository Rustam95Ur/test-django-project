from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings_list, name='setting_list'),
    path('save', views.save_or_update, name='setting_save_update'),
    path('delete/<int:setting_id>', views.setting_delete, name='setting_delete'),
    path('group/list', views.setting_groups_list, name='setting_groups_list'),
    path('group/save', views.setting_groups_save, name='save_update_setting_group'),
    path('group/delete/<int:group_id>', views.setting_groups_delete, name='setting_groups_delete'),
]
