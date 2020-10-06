from django.urls import path

from .views import index, info

app_name = 'weather'
urlpatterns = [
    path('', index, name='index'),
    path('<city>', info, name='info')
]
