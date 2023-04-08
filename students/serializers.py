from rest_framework import serializers
from django.contrib.auth.models import User

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
