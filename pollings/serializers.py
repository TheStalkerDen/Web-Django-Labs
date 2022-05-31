import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from pollings.models import Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name']


class AnswerSerializer(serializers.ModelSerializer):
    votes = serializers.ReadOnlyField(source='voters.count')

    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'votes']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    author_username = serializers.StringRelatedField(source='author')

    class Meta:
        model = Question
        fields = ['id', 'author', 'author_username', 'question_text', 'pub_date', 'answers']
        read_only_fields = ['id', 'pub_date']

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        question = Question.objects.create(author=validated_data["author"],
                                           question_text=validated_data['question_text'],
                                           pub_date=datetime.datetime.now())
        for answer in answers:
            Answer.objects.create(question=question, answer_text=answer["answer_text"])
        return question
