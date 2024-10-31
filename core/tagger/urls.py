from django.urls import path
from . import views


urlpatterns = [
    path('dataset/<int:dataset_id>/<int:tag_id>/', views.sentence_category, name='category'),
    
]
