from rest_framework import serializers

from .models import Dataset, Tag, Operator, HasPermission, Sentence, LabeledSentence


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Dataset


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class HasPermissionSerializer(serializers.ModelSerializer):
    dataset = serializers.SlugRelatedField(read_only=False, slug_field='name')
    class Meta:
        model = HasPermission
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    dataset = serializers.SlugRelatedField(read_only=False, slug_field='name')

    class Meta:
        model = Tag
        fields = '__all__'

class SentenceSerializer(serializers.ModelSerializer):
    dataset = serializers.SlugRelatedField(read_only=False, slug_field='name')
    class Meta:
        model = Sentence
        fields = '__all__'



class LabeledSentenceSerializer(serializers.ModelSerializer):
    dataset = serializers.SlugRelatedField(read_only=False, slug_field='name')
    sentence = serializers.SlugRelatedField(read_only=False, slug_field='body')
    tag = serializers.SlugRelatedField(read_only=False, slug_field='name')
    operator = serializers.SlugRelatedField(read_only=False, slug_field='user')
    class Meta:

        model = LabeledSentence
        fields = '__all__'