# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Subject, Teacher, Pupil, Grade
from src.marks.models import Lesson

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)
        
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('long_name', 'small_name')

class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('last_name', 'first_name', 'middle_name', 'sex', 'grade', 'group', 'special')

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('last_name', 'first_name', 'middle_name', 'grade', 'grades', 'subjects', 'administrator')
