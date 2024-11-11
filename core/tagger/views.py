from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import generics

from django.contrib.postgres.search import SearchVector

from .models import Dataset, Operator, HasPermission, Tag, LabeledSentence, Sentence
from .serializers import LabeledSentenceSerializer, TagSerializer, DatasetSerializer, \
    HasPermissionSerializer, SentenceSerializer, SentenceCSVSerializer
from .utils import read_sentences


# Create your views here.


class DatasetViewSet(ModelViewSet):
    """
    dataset viewset for super user to manage dataset instances.
    """
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

    def get(self, request, dataset_id, word, *args, **kwargs):
        """
        give it the word you want to search in labeled text body, dataset and tag
        """
        user = request.user
        word = word

        operator = Operator.objects.get(user=user)
        try:
            is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
        except HasPermission.DoesNotExist as _:
            return Response({"detail": "you don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
        if word is not None and word != '':
            items = LabeledSentence.objects.annotate(
                search=SearchVector('sentence__body', 'sentence__dataset__name', 'sentence__dataset__description',
                                    'tag__name')).filter(search=word)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LabelingSentenceAPIView(APIView):
    serializer_class = LabeledSentenceSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        you can label sentences with available tags for that dataset
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        t = serializer.validated_data['tag']  # Tag
        s = serializer.validated_data['sentence']  # sentence
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
        """
        list of not labeled sentence that user has permission to access for labeling.
        """
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

    def get(self, request, dataset_id, *args, **kwargs):
        """
        list of sentences in given dataset
        """
        sentences = Sentence.objects.filter(dataset__id=dataset_id)
        serializer = self.serializer_class(sentences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dataset_id, *args, **kwargs):
        """
        create sentence in specific dataset
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SentenceCSVAPIView(APIView):
    serializer_class = SentenceCSVSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        return Response({'data': 'upload a sentence csv file.'})

    def post(self, request, dataset_id, *args, **kwargs):
        """
        api for creating sentences with uploading a csv file of sentences.
        only admin has access to it.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            dataset = Dataset.objects.get(pk=dataset_id)
            decoded_file = file.read().decode('utf-8').splitlines()
            sentences = read_sentences(dataset, decoded_file)

            Sentence.objects.bulk_create(sentences)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
