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
    # update and delete permissions
    path('permission/<int:pk>/', views.PermissionUpdateDeleteView.as_view(), name='permission-detail'),
    # search inside dataset
    path('search/<int:dataset_id>', views.SearchLabeledSentenceAPIView.as_view(), name='search'),
    # labeling sentence
    path('label/', views.LabelingSentenceAPIView.as_view(), name='labeling'),
    # list and create Sentences
    path('dataset/<int:dataset_id>/sentence/', views.ListCreateSentencesAPIView.as_view(), name='list-create-sentence'),
    # upload csv file to create sentences
    path('sentence/csv/<int:dataset_id>/', views.SentenceCSVAPIView.as_view(), name='sentence-csv'),
]
urlpatterns += router.urls
