from django.urls import path
from . import views

urlpatterns = [
    path('', views.agents_login_list, name='agents_login_list'),
    path('view/<int:agent_id>', views.agent_login_view, name='agent_login_view'),
    path('report', views.login_report_page, name='login_report_page'),
    path('report/export', views.login_report_export, name='login_report_export'),

]