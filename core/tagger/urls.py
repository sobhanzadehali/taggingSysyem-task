from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'dataset', views.DatasetViewSet)

urlpatterns = [
    # list and create tag
    path('dataset/<int:dataset_id>/tags/', views.TagAPIView.as_view(), name='tag-list'),
    # lists sentences tagged with specific tag
    path('dataset/<int:dataset_id>/<int:tag_id>/', views.SentenceCategoryAPIView.as_view(), name='category'),
    # admin gives permission to operator
    path('permission/', views.PermissionAPIView.as_view(), name='permission'),
]
urlpatterns += router.urls
