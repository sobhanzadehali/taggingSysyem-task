from django.template.context_processors import request
from rest_framework import serializers

from .models import Dataset, Tag, Operator, HasPermission, Sentence, LabeledSentence


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'description',)
        model = Dataset


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class HasPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HasPermission
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = '__all__'


class LabeledSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabeledSentence
        fields = '__all__'
