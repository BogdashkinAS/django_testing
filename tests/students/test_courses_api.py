from rest_framework.test import APIRequestFactory
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from model_bakery import baker
import json
from students.models import Student, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.prepare(Student, *args, **kwargs)

    return factory

@pytest.fixture
def course_factory(students_factory):
    def factory(*args, **kwargs):
        students_set = students_factory(_quantity=3, _fill_optional=True)
        return baker.make(Course, students=students_set, *args, **kwargs, make_m2m=True)

    return factory


# проверка получения первого курса (retrieve-логика)

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_first_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    students_list = []

    # # Act
    response = client.get('/courses/')
    data = response.json()
    students = list(course[0].students.all())

    # Assert
    assert data[0]['id'] == course[0].id
    assert data[0]['name'] == course[0].name
    for student in students:
        students_list.append(str(student))
    assert data[0]['students'] == students_list
    assert response.status_code == 200



# проверка получения списка курсов (list-логика)

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_all_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=5)
    students_list = []
    
    # Act
    response = client.get('/courses/')
    data = response.json()
    
    # Assert
    assert len(data) == len(course)
    for i in range(len(course)):
        students_list = []
        assert data[i]['id'] == course[i].id
        assert data[i]['name'] == course[i].name
        students = list(course[i].students.all())
        for student in students:
            students_list.append(str(student))
        assert data[i]['students'] == students_list
    assert response.status_code == 200



# проверка фильтрации списка курсов по id

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_filter_id_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=5)
    students_list = []

    # Act
    response = client.get('/courses/?id=5')
    data = response.json()
    
    # Assert
    assert data[0]['id'] == course[4].id
    assert data[0]['name'] == course[4].name
    students = list(course[4].students.all())
    for student in students:
        students_list.append(str(student))
    assert data[0]['students'] == students_list
    assert response.status_code == 200
    


# проверка фильтрации списка курсов по name

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_filter_name_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=4)
    course2 = course_factory(name='Physics')
    course.append(course2)
    students_list = []

    # Act
    response = client.get('/courses/?name=Physics')
    data = response.json()
    
    # Assert
    assert len(course) == 5
    assert course[4].name == 'Physics'
    assert data[0]['name'] == 'Physics'
    assert data[0]['name'] == course[4].name
    students = list(course[4].students.all())
    for student in students:
        students_list.append(str(student))
    assert data[0]['students'] == students_list
    assert response.status_code == 200
    


# тест успешного создания курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_make_course(client):
    # Arrange
    data = {'name': 'Physics'}  

    # Act
    response = client.post('/courses/', data)
    data = response.json()
    
    # Assert
    assert data['id'] == 1
    assert data['name'] == 'Physics'
    assert response.status_code == 201


# тест успешного обновления курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_patch_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    records = {'name': 'Physics'}   
    students_list = []

    # Act
    response = client.patch('/courses/1/', records)
    data = response.json()
    
    # Assert
    assert data['id'] == 1
    assert data['name'] == 'Physics'
    assert course[0].name != data['name']
    students = list(course[0].students.all())
    for student in students:
        students_list.append(str(student))
    assert data['students'] == students_list
    assert response.status_code == 200
    
    
# тест успешного удаления курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_delete_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)

    # Act
    response = client.delete('/courses/1/')
    
    # Assert
    assert response.status_code == 204