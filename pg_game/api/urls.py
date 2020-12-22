from django.urls import path
from . import views


urlpatterns = [
    path('profile/get', views.get_profile, name='get_profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('profile/statistic', views.profile_statistic, name='profile_statistic'),
    path('ratings/<int:count>/<int:page>', views.get_ratings, name='get_ratings'),
    path('rating/<int:kpi_id>/<int:count>/<int:page>', views.get_rating_by_id, name='get_rating_by_id'),

    path('apk/check_version', views.check_version, name='check_apk_version'),
    path('apk/get_file/<str:type_apk>', views.get_apk, name='get_apk_file'),

]