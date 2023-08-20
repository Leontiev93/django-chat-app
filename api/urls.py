from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('conversations/start/', views.start_convo, name='start_convo'),
    path('conversations/<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('conversations/', views.conversations, name='conversations'),
    path('users/', views.user_list, name='user_list')

]
