from rest_framework import serializers

from students.models import Course, Student

# class StudentSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Student
#         fields = ("name", "birth_date")


class CourseSerializer(serializers.ModelSerializer):
    # students = StudentSerializer

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    
