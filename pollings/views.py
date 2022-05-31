from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from pollings.models import Question, Answer
from pollings.serializers import UserSerializer, QuestionSerializer, AnswerSerializer


def is_already_vote(question, user_id):
    for answer in question.answers.all():
        result_set = answer.voters.filter(pk=user_id)
        if result_set.count() != 0:
            return True
    return False


def you_have_already_vote_response():
    return Response({'status': 'bad', 'message': 'You have already vote on this question'},
                    status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, url_path='is-already-vote', permission_classes=[IsAuthenticated])
    def is_already_vote(self, request, pk=None):
        question = self.get_object()
        jwt_object = JWTAuthentication()
        user, _ = jwt_object.authenticate(request)
        if is_already_vote(question, user.id):
            return Response({'is-already-vote': True})
        return Response({'is-already-vote': False})


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['patch'])
    def vote(self, request, question_pk=None, pk=None):
        answer = self.get_object()
        question = Question.objects.get(pk=question_pk)
        jwt_object = JWTAuthentication()
        user, _ = jwt_object.authenticate(request)
        if is_already_vote(question, user.id):
            return you_have_already_vote_response()
        answer.voters.add(user.id)
        answer.save()
        return Response({'status': 'ok', 'message': 'Thank you for your vote'})
