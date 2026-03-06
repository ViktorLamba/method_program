from django.shortcuts import render
from django.http import HttpResponse, Http404
from catalog.data import COURSES, AUTHORS, INFO_TEXT


def index(request):
    """Главная страница"""
    context = {
        'title': 'Главная страница',
        'courses_count': len(COURSES),
        'authors_count': len(AUTHORS),
        'featured_courses': COURSES[:3]
    }
    return render(request, 'index.html', context)


def courses(request):
    """Список всех курсов"""
    context = {
        'title': 'Все курсы',
        'courses': COURSES
    }
    return render(request, 'courses.html', context)


def course_detail(request, course_id):
    """Страница курса"""
    course = None
    for c in COURSES:
        if c['id'] == course_id:
            course = c
            break

    if not course:
        raise Http404("Курс не найден")

    # Находим автора курса
    author = None
    for a in AUTHORS:
        if a['id'] == course['author_id']:
            author = a
            break
    
    context = {
        'title': course['title'],
        'course': course,
        'author': author
    }
    return render(request, 'course_detail.html', context)


def authors(request):
    """Список авторов"""
    context = {
        'title': 'Авторы курсов',
        'authors': AUTHORS
    }
    return render(request, 'authors.html', context)


def author_details(request, author_id):
    """Страница автора"""
    author = None
    for a in AUTHORS:
        if a['id'] == author_id:
            author = a
            break

    if not author:
        raise Http404("Автор не найден")

    # Находим курсы автора
    author_courses = [c for c in COURSES if c['author_id'] == author_id]

    context = {
        'title': author['name'],
        'author': author,
        'courses': author_courses
    }
    return render(request, 'author_details.html', context)


def info(request):
    """Страница информации"""
    context = {
        'title': 'Информация',
        'info_text': INFO_TEXT
    }
    return render(request, 'info.html', context)


def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, 'not_found.html', status=404)