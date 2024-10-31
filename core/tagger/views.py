from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Dataset, Operator, HasPermission, Tag, Sentence, LabeledSentence
from .serializers import LabeledSentenceSerializer


# Create your views here.


@api_view(['GET'])
def sentence_category(request, dataset_id, tag_id):
    """
    lists every labeled sentence inside a specific dataset with given tag.
    """
    user = request.user
    if not user.is_authenticated:
        return Response({"detail":"login first"},status=status.HTTP_401_UNAUTHORIZED)
    operator = Operator.objects.get(user=user)
    try:
        is_allowed = HasPermission.objects.get(operator=operator, dataset__pk=dataset_id)
    except HasPermission.DoesNotExist as e:
        return Response({"detail": "you don't have permission"},status=status.HTTP_400_BAD_REQUEST)
    if is_allowed:
        labelled_sentences = LabeledSentence.objects.filter(sentence__dataset=dataset_id,tag__pk=tag_id)
        serializer = LabeledSentenceSerializer(labelled_sentences, many=True)


        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)
