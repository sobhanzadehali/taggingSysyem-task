from re import search

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.contrib.postgres.search import SearchVector

from .models import Dataset, Operator, HasPermission, Tag, Sentence, LabeledSentence
from .serializers import LabeledSentenceSerializer, SentenceSerializer, TagSerializer, DatasetSerializer, \
    HasPermissionSerializer


# Create your views here.


class DatasetViewSet(ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = (IsAdminUser,)
    queryset = Dataset.objects.all()


class SentenceCategoryAPIView(APIView):
    serializer_class = LabeledSentenceSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, dataset_id, tag_id):
        """
            lists every labeled sentence inside a specific dataset with given tag.
        """
        user = request.user
        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as e:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        if is_allowed:
            labelled_sentences = LabeledSentence.objects.filter(sentence__dataset=dataset_id, tag__pk=tag_id)
            serializer = self.serializer_class(labelled_sentences, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)


class TagAPIView(APIView):
    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, dataset_id):
        """
        list all tages in a dataset if you have permission.
        """
        user = request.user
        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as e:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        tags = Tag.objects.filter(dataset__pk=dataset_id, is_active=True)
        serializer = self.serializer_class(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dataset_id):
        """
        create tag if you have permission.
        """
        user = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionAPIView(APIView):
    serializer_class = HasPermissionSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request):
        serializer = self.serializer_class(HasPermission.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchLabeledSentenceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LabeledSentenceSerializer

    def get(self, request, dataset_id):
        """
        
        """
        user = request.user
        q = request.GET.get('subject', None)
        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as e:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        if q is not None and q != '':
            items = LabeledSentence.objects.annotate(
                search=SearchVector('sentence__body', 'sentence__dataset__name', 'sentence__dataset__description',
                                    'tag__name')).filter(search=q)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
