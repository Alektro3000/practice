from rest_framework import serializers
from summary.models import SummaryFile

class SummaryFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SummaryFile
        fields = ['id', 'name','type','format']