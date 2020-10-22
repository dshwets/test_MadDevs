from rest_framework.serializers import ModelSerializer

from history_service.models import CommitsHistory


class CommitHistorySerializer(ModelSerializer):
        class Meta:
            model = CommitsHistory
            fields = '__all__'
            read_only_fields = ['link', 'commit_id', 'commit_json']
