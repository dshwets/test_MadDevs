from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from api_v1.serializers import CommitHistorySerializer
from history_service.models import CommitsHistory


class CommitsHistoryViewSet(ModelViewSet):
    queryset = CommitsHistory.objects.all()
    serializer_class = CommitHistorySerializer
