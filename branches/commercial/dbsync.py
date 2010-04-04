# -*- coding: UTF-8 -*-

import os
import sys
import time
import binascii
from datetime import datetime, timedelta

sys.path.insert(0, '/home/avisosms/lib/python2.5/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

dir = os.path.dirname(os.path.abspath(__file__))

from src.userextended.models import Pupil, Teacher, Grade, Staff

for p in Pupil.objects.all(): p.save()
for p in Teacher.objects.all(): p.save()
for p in Staff.objects.all(): p.save()







