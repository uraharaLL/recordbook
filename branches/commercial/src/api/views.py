# -*- coding: utf-8 -*-

import demjson
from hashlib import md5
from datetime import datetime, timedelta, date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.aggregates import Avg

import src
from src import settings
from src.userextended.models import School, Pupil, Teacher, Achievement
from src.library.models import Arrearage
from src.marks.models import Mark, ResultDate, Result
from src.attendance.models import UsalTimetable

from src.api import forms

def REST(request, model, id = 0):
    method = request.method
    
    models = settings.REST_MODELS
    Model = eval(settings.REST_MODELS2APPS[model][0])
    Form = eval(settings.REST_MODELS2APPS[model][1])

    status = 200
    render = u''
    headers = {}
    
#    status = 401
#    headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
    logined = False
    import base64
    from django.contrib.auth import authenticate, login
    if request.META.has_key('HTTP_HTTP_AUTHORIZATION'):
        auth = request.META['HTTP_HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                try:
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                except:
                    uname = passwd = ''
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active and user.is_superuser:
                        logined = True
                        login(request, user)
                        request.user = user
    if not logined:
        method = 'Auth'
    
    if method == 'GET':
        if id:
            model = get_object_or_404(Model, id = id)
            render = model.serialize(Model.serialize_fields)
        else:
            Model.objects.all()
            render = Model.objects.serialize(Model.serialize_fields)
    elif method == 'HEAD':
        if id:
            model = get_object_or_404(Model, id = id)
        else:
            model = Model.objects.all().order_by('-rest_modified')[0]
        headers['Modified'] = model.rest_modified.isoformat()
    elif method == 'POST':
        import demjson
        try:
            data = demjson.decode(request.raw_post_data)
        except:
            status = 406
            render = 'Wrong data'
            return HttpResponse(render, status = status)
        if id:
            model = get_object_or_404(Model, id = id)
        else:
            model = Model()
            status = 201
        form = Form(data, instance = model)
        if form.is_valid():
            form.save()
            if status == 201:
                headers['Location'] = model.get_absolute_uri()
        else:
            status = 406
            render = form.errors
    elif method == 'DELETE':
        if id:
            get_object_or_404(Model, id = id).delete()
        else:
            status = 406
    elif method == 'OPTIONS':
        headers['Allow'] = 'get, head, post, delete'.upper()
    elif method == 'Auth':
        status = 401
        headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
    else:
        status = 501
    
    response = HttpResponse(render, status = status)
    for header in headers.keys():
        response[header] = headers[header]

    return response


def terminalAuth(request):
    cart = str(request.GET.get('cart', ''))
    secret_key = 'fucking_hacking' + cart.lower()
    secret_key = md5(secret_key).hexdigest()
    error = {}
    pupil = None
    if (request.GET.get('secret_key', '') != secret_key) and not settings.DEBUG:
        error['code'] = 1
        error['error'] = 'Acces denided'
        error['error_ru'] = u'Доступ запрещён'
    if Pupil.objects.filter(cart = cart).count()==0:
        error['code'] = 2
        error['error'] = 'Pupil not finded'
        error['error_ru'] = u'Ученик не найден'
    else:
        pupil = Pupil.objects.get(cart = cart)
    return (error, pupil)


def terminalMain(request):
    render = {}
    
    #Init
    auth = terminalAuth(request)
    if len(auth[0]) == 0:
        pupil = auth[1]
    else:
        render['error'] = auth[0]
        return HttpResponse(demjson.encode(render))
    
    #Globals
    globals = {}
    globals['saturday'] = pupil.school.saturday
    globals['studentName'] = pupil.if_()
    globals['studentGroup'] = pupil.grade.long_name
    globals['studentPhoto'] = '/photos/%d.jpg' % pupil.id
    globals['points'] = pupil.get_marks_avg()
    globals['money'] = pupil.account
    globals['startTerm'] = '2010-01-11'
    globals['endTerm'] = '2010-03-31'
    render['globals'] = globals
    
    #Timetable
    timetable = {}
    for day in settings.WORKDAYS:
        if not pupil.school.saturday and day[0] == 6: continue
        timetable[day[0]] = {}
        for lesson in settings.LESSON_NUMBERS:
            if UsalTimetable.objects.filter(grade = pupil.grade, number = lesson[0], group = pupil.group, workday = day[0]).count() == 0:
                name = ''
                room = ''
            else:
                t = UsalTimetable.objects.get(grade = pupil.grade, number = lesson[0], group = pupil.group, workday = day[0])
                name = t.subject.name
                room = t.room
            timetable[day[0]][lesson[0]] = {'name': name, 'room': room}
    render['timetable']= timetable
    
    #Books
    books = []
    for arrearage in Arrearage.objects.filter(pupil = pupil):
        books.append({'id': arrearage.id,
                      'name': arrearage.book.name,
                      'author': arrearage.book.author,
                      'date': arrearage.owe_back.isoformat(),
                      'back': arrearage.back == None,
                    })
    render['books'] = books
    
    #Classmates
    render['classmates'] = [{'name': classmate.if_(), 'points': classmate.get_marks_avg()} for classmate in Pupil.objects.filter(grade = pupil.grade) if pupil.id != classmate.id]
    
    #Teachers
    teachers = []
    for teacher in pupil.get_teachers():
        teachers.append({'name': teacher.get_fio(),
                        'lessons': ', '.join([subject.name for subject in teacher.subjects.all()]),
                        'achievements': [],
#                        'achievements': [{'date': achievement.date.isoformat(), 'name': achievement.title, 'description': achievement.description} for achievement in Achievement.objects.filter(pupil = pupil)],
                       })
    render['teachers'] = teachers
    
    #Achievements
    render['achievements'] = [{'date': achievement.date.isoformat(), 'name': achievement.title, 'description': achievement.description} for achievement in Achievement.objects.filter(pupil = pupil)]
    
    #Weekends
    render['weekeds'] = ['2010-01-07', '2010-01-11']
    
    #Marks
    marks = []
    for subject in pupil.get_subjects():
        marks.append({'lesson': subject.name,
                      'marks': [{'date': mark.lesson.date.isoformat(), 'mark': mark.mark, 'absent': mark.absent} for mark in Mark.objects.filter(pupil = pupil, lesson__subject = subject, lesson__date__month = date.today().month, lesson__date__year = date.today().year) ] + [{'date': mark.resultdate.date.isoformat(), 'mark': mark.mark, 'absent': False} for mark in Result.objects.filter(pupil = pupil, subject = subject, resultdate__enddate__month = date.today().month, resultdate__enddate__year = date.today().year) ]
                      })
    render['marks'] = marks
    
    
    return HttpResponse(demjson.encode(render))
    

def terminalMarks(request):
    render = {}
    
    #Init
    auth = terminalAuth(request)
    if len(auth[0]) == 0:
        pupil = auth[1]
    else:
        render['error'] = auth[0]
        return HttpResponse(demjson.encode(render))
    month = request.GET.get('month', '')
    if len(month) != 7:
        error = {}
        error['code'] = 3
        error['error'] = 'Bad format'
        error['error_ru'] = u'Неверный формат даты'
        render['error'] = error
        return HttpResponse(demjson.encode(render))
    
    year = month[:4]
    month = month[5:]

    marks = []
    for subject in pupil.get_subjects():
        marks.append({'lesson': subject.name,
                      'marks': [{'date': mark.lesson.date.isoformat(), 'mark': mark.mark, 'absent': mark.absent} for mark in Mark.objects.filter(pupil = pupil, lesson__subject = subject, lesson__date__month = month, lesson__date__year = year) ] + [{'date': mark.resultdate.date.isoformat(), 'mark': mark.mark, 'absent': False} for mark in Result.objects.filter(pupil = pupil, subject = subject, resultdate__enddate__month = date.today().month, resultdate__enddate__year = date.today().year) ]
                      })
    render['marks'] = marks
    
    return HttpResponse(demjson.encode(render))

def terminalBook(request):
    render = {}
    
    #Init
    auth = terminalAuth(request)
    if len(auth[0]) == 0:
        pupil = auth[1]
    else:
        render['error'] = auth[0]
        return HttpResponse(demjson.encode(render))
    book = get_object_or_404(Arrearage, id = request.GET.get('id', 0), pupil = pupil)
    book.owe_back = book.owe_back + timedelta(weeks = 1)
    book.repeat += 1
    book.save()
    render['status'] = 'ok'
    
    return HttpResponse(demjson.encode(render))

def formatModel(s):
    return s[0].upper() + s[1:].lower()
    
    
