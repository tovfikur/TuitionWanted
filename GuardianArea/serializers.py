from rest_framework import serializers
from .models import GuardianDetails, Note, Child


class GuardianListSerializers(serializers.ModelSerializer):
    class Meta:
        model = GuardianDetails
        fields = '__all__'
        depth = 2


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
