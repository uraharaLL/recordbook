# -*- coding: UTF-8 -*-

import os
import sys
import time
import binascii
import csv
from datetime import datetime, timedelta

sys.path.insert(0, '/home/avisosms/lib/python2.5/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

dir = os.path.dirname(os.path.abspath(__file__))

from src.userextended.models import Pupil, Teacher, Grade, Staff, Subject, School
from src.attendance.models import UsalTimetable


school = School.objects.get(id = 6)

for o in Pupil.objects.filter(school = school):
    o.save()
    
for o in Teacher.objects.filter(school = school):
    o.save()

