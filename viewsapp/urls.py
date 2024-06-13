from django.urls import path
from .views import index, handle_generate_views

urlpatterns = [
    path('', index, name='index'),
    path('generateViews', handle_generate_views, name='generate_views'),
]
