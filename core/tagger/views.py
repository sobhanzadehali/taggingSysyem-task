from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import generics

from django.contrib.postgres.search import SearchVector

from .models import Dataset, Operator, HasPermission, Tag, LabeledSentence, Sentence
from .serializers import LabeledSentenceSerializer, TagSerializer, DatasetSerializer, \
    HasPermissionSerializer, SentenceSerializer


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
    """
    permission detail, update nad delete
    """
    serializer_class = HasPermissionSerializer
    permission_classes = (IsAdminUser,)
    queryset = HasPermission.objects.all()


class SearchLabeledSentenceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LabeledSentenceSerializer

    def get(self, request, dataset_id, *args, **kwargs):
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


class LabelingSentenceAPIView(APIView):
    serializer_class = LabeledSentenceSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        t =  serializer.validated_data['tag']# Tag
        s =  serializer.validated_data['sentence'] # sentence
        same_dataset = t.dataset.pk == s.dataset.pk

        if same_dataset:
            try:
                _ = HasPermission.objects.get(operator=Operator.objects.get(user=request.user),
                                              dataset__pk=s.dataset.pk)
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            except HasPermission.DoesNotExist as e:
                return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': " you can't give that tag to this sentence, it is not defined!"},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        authorized_datasets = HasPermission.objects.filter(operator=Operator.objects.get(user=request.user))
        dataset_ids = list(authorized_datasets.values_list('dataset__pk', flat=True))
        labeled_sentences = LabeledSentence.objects.all()
        sentences = Sentence.objects.filter(dataset__id__in=dataset_ids).exclude(
            id__in=labeled_sentences.values_list('sentence__id', flat=True))

        serializer = SentenceSerializer(sentences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateSentencesAPIView(APIView):
    serializer_class = SentenceSerializer
    permission_classes = (IsAdminUser,)

    def get(self,request, dataset_id, *args, **kwargs):
        sentences = Sentence.objects.filter(dataset__id=dataset_id)
        serializer = self.serializer_class(sentences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

    def post(self, request, dataset_id, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


