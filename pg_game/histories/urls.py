from django.urls import path
from . import views

urlpatterns = [
    path('', views.history_page, name='home'),
    path('file_upload', views.history_file_upload, name='file_upload'),
    path('file_save', views.history_file_save, name='file_save'),
    path('history/agents', views.agents_history, name='agents_history'),
    path('history/agent/<int:agent_id>', views.agent_history, name='agent_history'),
    path('history/agent/update-image', views.agent_update_image, name='agent_update_image')
]
