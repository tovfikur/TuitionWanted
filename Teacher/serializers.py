from rest_framework import serializers
from Teacher.models import Teacher, Subject, TeachingSection, Areas, Division, District, Thana


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class ThanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thana
        fields = '__all__'


class TeacherListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 2


class TeacherListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TeachingSectionAPI(serializers.ModelSerializer):
    class Meta:
        model = TeachingSection
        fields = '__all__'


class AreasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'

