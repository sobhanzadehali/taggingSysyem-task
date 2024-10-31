from django.urls import path
from . import views


urlpatterns = [
    # list and create tag
    path('dataset/<int:dataset_id>/tags/', views.TagAPIView.as_view(), name='tag-list'),
    # lists sentences tagged with specific tag
    path('dataset/<int:dataset_id>/<int:tag_id>/', views.SentenceCategoryAPIView.as_view(), name='category'),

]
