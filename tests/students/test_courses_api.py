from django.urls import reverse
import pytest
# from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker

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
        students_set = students_factory(_quantity=3, _fill_optional=True, name='Smith')
        return baker.make(Course, students=students_set, *args, **kwargs, make_m2m=True)

    return factory


# проверка получения первого курса (retrieve-логика)

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_first_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1, name='name1')

    # # Act
    response = client.get('/courses/')
    # response = client.get(reverse('courses-list'))
    data = response.json()

    # Assert
    for i in data[0]['students']:
        print(i)
    assert data[0]['id'] == course[0].id
    assert data[0]['name'] == course[0].name
    assert response.status_code == 200

    # assert [f'{st.name}, {st.birth_date}' for st in course[0].students.all()] == [st for st in response.json()[0]['students']]
    # for dat in data:
    #     print(dat)
    # for i in course[0].students.all():
    #     print(f'Имя: {i.name}')
    #     print(f'Дата: {i.birth_date}')
    # assert course[0].name == '5'
    # assert data[0]['students'][0].id == '000'
    # assert course[0].students.all() == '000'
    
    


# проверка получения списка курсов (list-логика)

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_all_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=5)

    # Act
    response = client.get('/courses/')
    data = response.json()
    
    # Assert
    assert len(data) == len(course)
    for i in range(len(course)):
        assert data[i]['id'] == course[i].id
        assert data[i]['name'] == course[i].name
        assert response.status_code == 200
    


# # проверка фильтрации списка курсов по id

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_filter_id_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=5)

    # Act
    response = client.get('/courses/?id=5')
    data = response.json()
    
    # Assert
    assert data[0]['id'] == course[4].id
    assert response.status_code == 200
    


# # проверка фильтрации списка курсов по name

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_get_filter_name_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=4)
    course2 = course_factory(name='Physics')
    course.append(course2)

    # Act
    response = client.get('/courses/?name=Physics')
    data = response.json()
    
    # Assert
    assert len(course) == 5
    assert course[4].name == 'Physics'
    assert data[0]['name'] == 'Physics'
    assert data[0]['name'] == course[4].name
    assert response.status_code == 200
    


# # тест успешного создания курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_make_course(client):
    # Arrange
    records = {'name': 'Physics'}   

    # Act
    response = client.post('/courses/', records)
    data = response.json()
    
    # Assert
    assert data['id'] == 1
    assert data['name'] == 'Physics'
    assert response.status_code == 201


# # тест успешного обновления курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_patch_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    records = {'name': 'Physics'}   

    # Act
    response = client.patch('/courses/1/', records)
    data = response.json()
    
    # Assert
    assert data['id'] == 1
    assert data['name'] == 'Physics'
    assert course[0].name != data['name']
    assert response.status_code == 200
    
    
# # тест успешного удаления курса

@pytest.mark.django_db(transaction=True, reset_sequences=True) # подключение тестовой БД
def test_delete_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)

    # Act
    response = client.delete('/courses/1/')
    
    # Assert
    assert response.status_code == 204
    