from rest_framework.response import Response
from rest_framework import serializers
from GuardianArea.models import GuardianDetails, ChildGroup, Child
from Teacher.models import Teacher
from .models import GuardianHistory, TeacherHistory, \
    TemporaryTuitionForChild, \
    PermanentTuitionForChild, \
    ShortListedTuitionForChild, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class ChildSerializerRetrive(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 2


class GuardianListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardianDetails
        fields = '__all__'
        depth = 2


class GuardianUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardianDetails
        fields = '__all__'


class GuardianHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardianHistory
        fields = [
            'Child',
            'Teacher',
            'Salary'
        ]
        depth = 2


class ChildGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildGroup
        fields = '__all__'


class TeacherDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 2


class TeacherHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherHistory
        fields = [
            'id',
            'Salary',
            'Starting_Date',
            'Ending_Date',
            'Note',
            'Child'
        ]
        depth = 2


class TemporaryTuitionForChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryTuitionForChild
        fields = '__all__'
        depth = 2


class ShortlistTuitionForChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortListedTuitionForChild
        fields = '__all__'
        depth = 2


class ShortlistTuitionForChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortListedTuitionForChild
        fields = '__all__'
        # depth = 2


class PermanentTuitionForChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentTuitionForChild
        fields = '__all__'
        depth = 2


