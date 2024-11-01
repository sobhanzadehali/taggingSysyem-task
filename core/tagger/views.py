from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.contrib.postgres.search import SearchVector

from .models import Dataset, Operator, HasPermission, Tag, LabeledSentence
from .serializers import LabeledSentenceSerializer, TagSerializer, DatasetSerializer, \
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
        except HasPermission.DoesNotExist as _:
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
        list all tags in a dataset if you have permission.
        """
        user = request.user
        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as _:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        tags = Tag.objects.filter(dataset__pk=dataset_id, is_active=True)
        serializer = self.serializer_class(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dataset_id):
        """
        create tag if you have permission.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionAPIView(APIView):
    serializer_class = HasPermissionSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request):
        """
        list of dataset permissions
        """
        serializer = self.serializer_class(HasPermission.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        creating new dataset permission
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HasPermissionSerializer
    permission_classes = (IsAdminUser,)
    queryset = HasPermission.objects.all()



class SearchLabeledSentenceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LabeledSentenceSerializer

    def get(self, request, dataset_id, *args,**kwargs):
        """
        domain/api/{{dataset_id}}?word={{target_word_for_search}}
        search in labeled text body, dataset, tag        
        """
        user = request.user
        parameter = request.query_params.get('word', None)

        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as _:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        if parameter is not None and parameter != '':
            items = LabeledSentence.objects.annotate(
                search=SearchVector('sentence__body', 'sentence__dataset__name', 'sentence__dataset__description',
                                    'tag__name')).filter(search=parameter)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
